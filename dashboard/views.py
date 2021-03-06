from itertools import chain

from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from links.models import Website, Channel, Group, Instagram
from .forms import (
    SelectLinkForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .mixins import UserMixIn, ReplaceChildWithParent
from .models import Action
from . import utils


User = get_user_model()


def get_paginated_object_list(request, queryset, num):
    paginator = Paginator(queryset, num)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return object_list, page


# list latest user's links: websites, channels, groups, and instagrams
@login_required
def index(request):
    user = request.user
    sorted_links = utils.get_sorted_users_links(user)
    # if links have child, sent their child instead of them.
    links_and_children = utils.replace_child_with_parent(sorted_links)

    object_list, page = get_paginated_object_list(request,
                                        links_and_children, 10)

    context = {
        'links': object_list,
        'page': page,
        'is_paginated': True,
        'active_dashboard': True,
    }
    return render(request, 'dashboard/index.html', context)


# guide
@login_required
def rules(request):
    return render(request, 'dashboard/rules.html', {'active_dashboard': True})


# add link
@login_required
def add_link(request):
    link_type = request.POST.get('link_type')
    if link_type == 'website':
        return redirect('links:website-create')
    elif link_type == 'channel':
        return redirect('links:channel-create')
    elif link_type == 'group':
        return redirect('links:group-create')
    elif link_type == 'instagram':
        return redirect('links:instagram-create')
    else:
        form = SelectLinkForm()

        if not request.user.is_premium:
            # remove website from choices if user is not `premium`
            choices = form.fields.get('link_type').choices
            choices.remove(('website', _('Website')))
            form.fields.get('link_type').choices = choices

        context = {
            'form': form,
            'active_addlink': True,
        }
        return render(request, 'dashboard/add_link.html', context)


# list user's websites
class UserWebsiteListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Website
    template_name = 'dashboard/users_websites.html'


# list user's channels
class UserChannelListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Channel
    template_name = 'dashboard/users_channels.html'


# list user's groups
class UserGroupListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Group
    template_name = 'dashboard/users_groups.html'


# list user's instagrams
class UserInstagramListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Instagram
    template_name = 'dashboard/users_instagrams.html'


def register(request):
    # redirect logged in users to their dashboard
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # create user
            messages.success(request,
                _('Your account has been created! You are now able to log in')
            )
            return redirect('dashboard:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'dashboard/user_update.html'
    success_url = reverse_lazy('dashboard:index')
    success_message = _('Your account has been updated')

    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
    ]

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


@login_required
def recent_actions(request):
    user = request.user
    if not (user.is_superuser or user.is_staff):
        # none admin users won't be able to see this view/page
        raise PermissionDenied

    recent_actions = Action.objects.filter(is_read=False)
    object_list, page = get_paginated_object_list(request, recent_actions, 5)
    context = {
        'object_list': object_list,
        'page': page,
        'is_paginated': True,
        'active_dashboard': True,
    }
    return render(request, 'dashboard/recent_actions.html', context)
