import re
import os
import datetime

from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
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

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	UpdateAPIView,
    GenericAPIView,
)

from . import utils


class ApplicationMixIn(ListView):
    """
    This MixIn filters the queryset by application name,
    published and parent objects.
    `model` property must be set in the class base view.
    """
    paginate_by = 20

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
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.url = utils.add_slash(obj.url)
        obj.save()
        utils.create_or_update_action(obj, 'link created')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class CreateAPIMixIn(CreateAPIView):
    def perform_create(self, serializer):
        url = serializer.validated_data.get('url')
        instance = serializer.save(author=self.request.user,
            url=utils.add_slash(url))
        utils.create_or_update_action(instance, 'link created')


class PublishedObjectMixIn(UserPassesTestMixin):
    """
    Only published objects are allowed to be seen.
    But if the object belongs to current user, let user sees the object.

    eg: parent: published, child: published -> return parent

    eg: parent: published, child: draft ->
        return parent for non-owners, and child for the owners

    eg: parent: draft, child: None (not created yet) ->
            return parent for the owners
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
        return utils.get_parent_or_child_object(self)


class RetrieveUpdateAPIMixIn(RetrieveUpdateAPIView):
    def perform_update(self, serializer):
        obj = self.get_object()
        data = serializer.validated_data
        if not utils.validate_and_update_link(obj, data):
            raise utils.serialize_validation_exceptions[obj.model_name]
        return serializer

    def get_object(self):
        obj = utils.get_parent_or_child_object(self)
        # raise permission error if user don't have update permission
        self.check_object_permissions(self.request, obj)
        return obj


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
        obj = self.model.objects.get(slug=slug, parent=None)
        return obj

    # send flash message and do the rest (deleting the thumbnail then the link)
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        utils.delete_images(obj)
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)


class DeleteAPIMixIn(DestroyAPIView):
    def perform_destroy(self, instance):
        obj = self.get_object()
        utils.delete_images(obj)
        super().perform_destroy(instance)

    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = self.model.objects.get(slug=slug, parent=None)
        # raise permission error if user don't have delete permission
        self.check_object_permissions(self.request, obj)
        return obj


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


class FilterByTypeMixIn:
    """
    Filter queryset by `type`
    """

    def get_queryset(self):
        type = self.request.GET.get('type')
        queryset = super().get_queryset()
        if type:
            queryset = super().get_queryset().filter(type=type)
        return queryset


class FilterByApplicationMixIn:
    """
    Filter queryset by `application`
    """

    def get_queryset(self):
        app = self.request.GET.get('app')
        queryset = super().get_queryset()
        if app:
            queryset = super().get_queryset().filter(application=app)
        return queryset


class PaginateMixIn:
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        result = {
            'links': queryset,
        }
        return Response(result)
