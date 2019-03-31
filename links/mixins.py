import re
import os
import datetime

from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext, ugettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from . import utils


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
        Call set_tags() function to set tags of the links.
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        utils.create_or_update_action(self.object, 'link created')
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

        # if both parent and child are in published status, return parent
        # this only happens if object was modified in admin area
        if object.status == 'published':
            if object.child and object.child.status == 'published':
                return object

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

        if not utils.link_updated(object, cd, self.fields):
            return redirect(object.get_absolute_url())

        # if updating link wasn't successful raise exception
        if not utils.validate_and_update_link(object, cd):
            raise utils.validation_exceptions[object.model_name]

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
