from copy import deepcopy
import re
import os
import datetime

from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext, ugettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files import File


class ApplicationMixIn(ListView):
    """
    This MixIn filters the queryset by application name
    `model` property must be set in the class base view.
    """
    def get_queryset(self):
        """
        Get published object with the specific application
        """
        return self.model.objects.filter(application=self.application,
            status='published')


class CreateMixIn(CreateView):
    def form_valid(self, form):
        """
        On validation set the author of the link,
        Also call set_tags() function to set tags of the post
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        self.object.tags.add(self.object.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class PublishedObjectMixIn(UserPassesTestMixin):
    def test_func(self):
        self.object = self.get_object()
        return self.object.status == 'published'


class OwnerMixin(UserPassesTestMixin):
    """Test if user tries to delete their or others links"""
    def test_func(self):
        self.object = self.get_object()
        return (self.request.user == self.object.author)


class UpdateMixIn(UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        # make a copy of the first object on the second one
        update_copy(self, instance)
        return redirect(reverse_lazy('dashboard:index'))


class DeleteMixIn(LoginRequiredMixin, OwnerMixin, DeleteView):
    """This MixIn deletes an object"""
    success_url = reverse_lazy('dashboard:index')

    # redirect get request to success-url (dashboard-index)
    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    # send flash message and do the rest (deleting the thumbnail then the link)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_dup = self.model.objects.get(uuid=self.object.uuid)
        object_dup.delete()

        # remove object image and thumbnail image
        os.remove(self.object.image.path)
        os.remove(self.object.get_thumbnail_path())

        # remove duplicate object image and thumbnail image
        if self.object.image.name != object_dup.image.name:
            os.remove(object_dup.image.path)
            os.remove(object_dup.get_thumbnail_path())

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
