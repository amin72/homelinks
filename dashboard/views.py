from itertools import chain

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from links.models import Website, Channel, Group, Instagram
from .forms import SelectLinkForm
from .mixins import UserMixIn


# list latest user's links: websites, channels, groups, and instagrams
@login_required
def index(request):
    user = request.user
    websites = Website.objects.filter(author=user)
    channels = Channel.objects.filter(author=user)
    groups = Group.objects.filter(author=user)
    instagrams = Instagram.objects.filter(author=user)

    links = sorted(chain(channels, groups, instagrams),
        key=lambda link: link.created, reverse=True)

    # pagination
    paginator = Paginator(links, 10)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        'links': links,
        'page': page,
        'is_paginated': True,
    }
    return render(request, 'dashboard/index.html', context)


# guide
@login_required
def rules(request):
    return render(request, 'dashboard/rules.html')


# add link
@login_required
def add_link(request):
    link_type = request.POST.get('link_type')
    if link_type == 'channel':
        return redirect('links:channel-create')
    elif link_type == 'group':
        return redirect('links:group-create')
    elif link_type == 'instagram':
        return redirect('links:instagram-create')
    else:
        form = SelectLinkForm()
        return render(request, 'dashboard/add_link.html', {'form': form})


# list user's channels
class UserChannelsListView(LoginRequiredMixin, UserMixIn, ListView):
    model = Channel
    template_name = 'dashboard/users_channels.html'


# list user's groups
class UserGroupsListView(LoginRequiredMixin, UserMixIn, ListView):
    model = Group
    template_name = 'dashboard/users_groups.html'


# list user's instagrams
class UserInstagramsListView(LoginRequiredMixin, UserMixIn, ListView):
    model = Instagram
    template_name = 'dashboard/users_instagrams.html'
