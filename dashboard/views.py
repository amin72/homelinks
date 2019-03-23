from itertools import chain

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.translation import gettext, gettext_lazy as _

from links.models import Website, Channel, Group, Instagram
from .forms import (
    SelectLinkForm,
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm
)
from .mixins import UserMixIn, ReplaceChildWithParent
from .models import Profile


# list latest user's links: websites, channels, groups, and instagrams
@login_required
def index(request):
    user = request.user
    websites = Website.objects.filter(author=user, parent=None)
    channels = Channel.objects.filter(author=user, parent=None)
    groups = Group.objects.filter(author=user, parent=None)
    instagrams = Instagram.objects.filter(author=user, parent=None)

    links = sorted(chain(websites, channels, groups, instagrams),
        key=lambda link: link.created, reverse=True)

    # if links have child, sent their child instead of them.
    links_and_children = []
    for link in links:
        child = link.child
        if child:
            links_and_children.append(child)
        else:
            links_and_children.append(link)

    # pagination
    paginator = Paginator(links_and_children, 10)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

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

        if not request.user.profile.vip:
            # remove website from choices if user is not `vip`
            choices = form.fields.get('link_type').choices
            choices.remove(('website', 'Website'))
            form.fields.get('link_type').choices = choices

        context = {
            'form': form,
            'active_addlink': True,
        }
        return render(request, 'dashboard/add_link.html', context)


# list user's websites
class UserWebsitesListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Website
    template_name = 'dashboard/users_websites.html'


# list user's channels
class UserChannelsListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Channel
    template_name = 'dashboard/users_channels.html'


# list user's groups
class UserGroupsListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Group
    template_name = 'dashboard/users_groups.html'


# list user's instagrams
class UserInstagramsListView(LoginRequiredMixin,
    ReplaceChildWithParent,
    UserMixIn,
    ListView):
    model = Instagram
    template_name = 'dashboard/users_instagrams.html'


def register(request):
    # redirect logged in users to their dashboard
    if request.user.is_authenticated:
        return redirect(reverse_lazy('dashboard:index'))

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # create user and profile
            messages.success(request,
                _('Your account has been created! You are now able to log in')
            )
            return redirect('dashboard:login')
    else:
        form = UserRegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})


@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
            instance=request.user.profile)
        print('XXXXXX:', user_form.errors)
        print('YYYYYY:', profile_form.errors)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your account has been updated'))
            return redirect('dashboard:index')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'dashboard/update_user_info.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'active_dashboard': True,
    })
