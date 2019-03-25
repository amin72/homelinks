from copy import deepcopy
import re
import os
import datetime

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext, ugettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

from . import utils
from dashboard.models import Action


class ApplicationMixIn(ListView):
    """
    This MixIn filters the queryset by application name,
    published and parent objects.
    `model` property must be set in the class base view.
    """
    def get_queryset(self):
        """
        Get published object with the specific application
        """
        return self.model.objects.filter(
            application=self.application,
            status='published',
            parent=None)


class CreateMixIn(CreateView):
    def form_valid(self, form):
        """
        On validation set the author of the link,
        Create Action object for admins,
        Call set_tags() function to set tags of the links.
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        self.object.tags.add(self.object.title)

        # create action
        model_name = self.model.__name__.lower()
        content_type = ContentType.objects.get(model=model_name,
            app_label='links')
        Action.objects.get_or_create(type='link created',
            content_type=content_type, object_id=self.object.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class PublishedObjectMixIn(UserPassesTestMixin):
    """
    Only published objects are allowed to be seen.
    But if the object belongs to current user, let user sees the object.
    """

    def get_object(self):
        slug = self.kwargs.get("slug")
        queryset = self.model.objects.filter(slug=slug)
        object = queryset.first()

        # for the owner, let them see the child object (updated object)
        if object and object.author == self.request.user and object.child:
            object = object.child
        return object

    def test_func(self):
        self.object = self.get_object()
        if self.object is None:
            raise Http404
        elif self.object.author == self.request.user:
            return True
        else:
            return self.object.status == 'published'


class OwnerMixin(UserPassesTestMixin):
    """Test if user tries to delete their or others links"""
    def test_func(self):
        self.object = self.get_object()
        return (self.request.user == self.object.author)


class UpdateMixIn(UpdateView):
    def form_valid(self, form):
        cd = form.cleaned_data
        object = self.get_object()

        # check if values are the same before and after updating
        # if none of the values changed do not create child or update it
        for field in self.fields: # check all form fields
            if hasattr(object, field):
                value = getattr(object, field)
                if cd.get(field) != value:
                    break
        else:
            # object values are the same, redirect
            return redirect(object.get_absolute_url())

        # Create child if child does not exist.
        if object.parent:
            object_dup = object # update child
        else:
            object_dup = self.get_object() # create a child
            object_dup.pk = None
            object_dup.save()
            object_dup.parent = object

        # Assign all values that are sent with form to child.

        # channel, group object have application attribute
        if hasattr(object_dup, 'application'):
            object_dup.application = cd.get('application')

        # channel object
        if hasattr(object_dup, 'channel_id'):
            object_dup.channel_id = cd.get('channel_id')

        # instagram object
        if hasattr(object_dup, 'page_id'):
            object_dup.page_id = cd.get('page_id')

        # set slug and url for channel, group, instagram
        model_name = object_dup.__class__.__name__.lower()
        url = cd.get('url')
        if model_name == 'website':
            object_dup.url = url
            domain, ext = utils.split_http(url).split('.')
            slug = f'{domain}-{ext}'
            self.slug = slugify(slug)
        elif model_name == 'channel':
            utils.check_channel_id(object_dup.channel_id,
                object_dup.application)
            object_dup.url = utils.generate_channel_url(object_dup.channel_id,
                object_dup.application)
            object_dup.slug = slugify(
                f'{object_dup.application}-{object_dup.channel_id}')
        elif model_name == 'group':
            utils.check_duplicate_url(object_dup)
            slug = \
                f'{object_dup.application}-{object_dup.title}-{object_dup.uuid}'
            self.slug = slugify(slug)
        elif model_name == 'instagram':
            object_dup.url = utils.generate_instagram_url(object_dup.page_id)
            object_dup.slug = slugify(f'{object_dup.page_id}')

        # check for duplicate url
        utils.check_duplicate_url(object_dup)

        object_dup.title = cd.get('title')
        object_dup.category = cd.get('category')
        object_dup.description = cd.get('description')
        object_dup.status = 'draft'

        # save old image and thumbnail path
        old_dup_image_path = object_dup.image.path
        old_dup_thumbnail_path = object_dup.thumbnail_path
        object_dup.image = cd.get('image')

        # set tags
        for tag in object.tags.all():
           object_dup.tags.set(tag)
        object_dup.tags = None

        object_dup.save()

        # remove unused image and thumbnail
        if object_dup.image.path != old_dup_image_path and \
            object.image.path != old_dup_image_path:
            os.remove(old_dup_image_path)
            os.remove(old_dup_thumbnail_path)

        # create action
        content_type = ContentType.objects.get(model=model_name,
            app_label='links')
        Action.objects.get_or_create(type='link updated',
            content_type=content_type, object_id=self.object.id)

        messages.info(self.request, self.success_message)
        return redirect(object.get_absolute_url())

    def get_object(self):
        slug = self.kwargs.get('slug')
        # if result is 1 object, only parent object is present
        # if result is 2 objects, parent and child are present
        queryset = self.model.objects.filter(slug=slug)
        self.object = queryset.first() # get parent object
        child = self.object.child
        if child:
            return child
        return self.object


class DeleteMixIn(LoginRequiredMixin, OwnerMixin, DeleteView):
    """
    This MixIn deletes an object
    `success_message` property in sub class is required.
    """
    success_url = reverse_lazy('dashboard:index')

    # redirect get request to success-url (dashboard-index)
    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def get_object(self):
        slug = self.kwargs.get('slug')
        object = self.model.objects.get(slug=slug, parent=None)
        return object

    # send flash message and do the rest (deleting the thumbnail then the link)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            # remove image and thumbnail
            os.remove(self.object.image.path)
            os.remove(self.object.thumbnail_path)

            # if object has child remove child's image and thumbnail too
            child = self.object.child
            if child:
                os.remove(child.image.path)
                os.remove(child.thumbnail_path)
        except FileNotFoundError:
            pass

        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)


class InfoMessageMixin:
    """
    Add a info message on successful form submission.
    """
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.info(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class SetModelNameMixIn:
    """
    `model_name` property must be set in the sub class.
    """
    model_name = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model_name'] = self.model_name
        return context


class SetActiveCssClassMixIn:
    """
    This mixin is used for setting `active` attribute in html entities.
    `model_name` property must be set in sub class.
    """

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        key = f'active_{self.model_name}s'
        context[key] = True # eg. active_websites = True
        return context
