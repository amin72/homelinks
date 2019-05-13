from itertools import chain
from urllib.parse import unquote

from django.http import HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from taggit.models import Tag
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from ratelimit.mixins import RatelimitMixin
from ratelimit.decorators import ratelimit

from .models import (
    Category,
    Website,
    Channel,
    Group,
    Instagram,
    Report,
)

from .mixins import (
    ApplicationMixIn,
    PublishedObjectMixIn,
    LoginRequiredMixin,
    InfoMessageMixin,
    CreateMixIn,
    OwnerMixin,
    UpdateMixIn,
    DeleteMixIn,
    SuccessMessageMixin,
    SetModelNameMixIn,
    SetActiveCssClassMixIn,
)

from .forms import (
    CreateWebsiteForm,
    CreateChannelForm,
    CreateGroupForm,
    CreateInstagramForm,
    ReportForm,
)

from . import utils


# list all links: websites, channels, groups, and instagrams
def index(request):
    websites = Website.published.all()[:6]
    channels = Channel.published.all()[:6]
    groups = Group.published.all()[:6]
    instagrams = Instagram.published.all()[:6]

    context = {
        'websites': websites,
        'channels': channels,
        'groups': groups,
        'instagrams': instagrams,
        'active_home': True,
    }
    return render(request, 'links/index.html', context)


class WebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published websites"""
    model_name = 'website'
    queryset = Website.published.all()
    paginate_by = utils.MAX_PAGE_LIMIT


class IranianWebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published and iranian websites"""
    model_name = 'website'
    paginate_by = utils.MAX_PAGE_LIMIT

    def get_queryset(self):
        return Website.published.filter(type='iranian')


class ForeignWebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published and foreign websites"""
    model_name = 'website'
    paginate_by = utils.MAX_PAGE_LIMIT

    def get_queryset(self):
        return Website.published.filter(type='foreign')


class WebsiteDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    """
    Give detail about published object
    """
    model = Website
    lookup_field = 'slug'
    model_name = 'website'


class WebsiteCreateView(RatelimitMixin, LoginRequiredMixin,
                        InfoMessageMixin, CreateMixIn):
    model = Website
    success_message = utils.CREATE_MESSAGE
    fields = (
        'title',
        'url',
        'type',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '30/h'
    ratelimit_block = False
    ratelimit_method = 'POST'


class WebsiteUpdateView(RatelimitMixin, LoginRequiredMixin,
                        OwnerMixin, UpdateMixIn):
    model = Website
    success_message = utils.UPDATE_MESSAGE
    fields = (
        'title',
        'url',
        'type',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_method = 'POST'



class WebsiteDeleteView(DeleteMixIn):
    model = Website
    success_message = utils.DELETE_MESSAGE
## -----------------------------------------------------


class ChannelListView(SetActiveCssClassMixIn, ListView):
    queryset = Channel.published.all().filter(parent=None)
    model_name = 'channel'
    paginate_by = utils.MAX_PAGE_LIMIT


class TelegramChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='telegram'
    model_name = 'channel'


class SoroushChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='soroush'
    model_name = 'channel'


class GapChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='gap'
    model_name = 'channel'


class IGapChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='igap'
    model_name = 'channel'


class EitaaChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='eitaa'
    model_name = 'channel'


class ChannelDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Channel
    lookup_field = 'slug'
    model_name = 'channel'


class ChannelCreateView(RatelimitMixin, LoginRequiredMixin,
                        InfoMessageMixin, CreateMixIn):
    model = Channel
    success_message = utils.CREATE_MESSAGE
    fields = (
        'application',
        'title',
        'channel_id',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '30/h'
    ratelimit_block = False
    ratelimit_method = 'POST'


class ChannelUpdateView(RatelimitMixin, LoginRequiredMixin,
                        OwnerMixin, UpdateMixIn):
    model = Channel
    success_message = utils.UPDATE_MESSAGE
    fields = (
        'application',
        'title',
        'channel_id',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_method = 'POST'


class ChannelDeleteView(DeleteMixIn):
    model = Channel
    success_message = utils.DELETE_MESSAGE
## -----------------------------------------------------


class GroupListView(SetActiveCssClassMixIn, ListView):
    queryset = Group.published.all()
    model_name = 'group'
    paginate_by = utils.MAX_PAGE_LIMIT


class WhatsappGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application = 'whatsapp'
    model_name = 'group'


class TelegramGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='telegram'
    model_name = 'group'


class SoroushGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='soroush'
    model_name = 'group'


class GapGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='gap'
    model_name = 'group'


class IGapGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='igap'
    model_name = 'group'


class EitaaGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='eitaa'
    model_name = 'group'


class GroupDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Group
    lookup_field = 'slug'
    model_name = 'group'


class GroupCreateView(RatelimitMixin, LoginRequiredMixin,
                        InfoMessageMixin, CreateMixIn):
    model = Group
    success_message = utils.CREATE_MESSAGE
    fields = (
        'application',
        'title',
        'url',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '30/h'
    ratelimit_block = False
    ratelimit_method = 'POST'


class GroupUpdateView(RatelimitMixin, LoginRequiredMixin,
                        OwnerMixin, UpdateMixIn):
    model = Group
    fields = (
        'application',
        'title',
        'url',
        'category',
        'description',
        'image'
    )
    success_message = utils.UPDATE_MESSAGE
    ratelimit_key = 'user'
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_method = 'POST'


class GroupDeleteView(DeleteMixIn):
    model = Group
    success_message = utils.DELETE_MESSAGE
## -----------------------------------------------------


class InstagramListView(SetActiveCssClassMixIn, ListView):
    queryset = Instagram.published.all()
    model_name = 'instagram'
    paginate_by = utils.MAX_PAGE_LIMIT


class InstagramDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Instagram
    lookup_field = 'slug'
    model_name = 'instagram'


class InstagramCreateView(RatelimitMixin, LoginRequiredMixin,
                            InfoMessageMixin, CreateMixIn):
    model = Instagram
    success_message = utils.CREATE_MESSAGE
    fields = (
        'title',
        'page_id',
        'category',
        'description',
        'image'
    )
    ratelimit_key = 'user'
    ratelimit_rate = '30/h'
    ratelimit_block = False
    ratelimit_method = 'POST'


class InstagramUpdateView(RatelimitMixin, LoginRequiredMixin,
                            OwnerMixin, UpdateMixIn):
    model = Instagram
    fields = (
        'title',
        'page_id',
        'category',
        'description',
        'image'
    )
    success_message = utils.UPDATE_MESSAGE
    ratelimit_key = 'user'
    ratelimit_rate = '5/m'
    ratelimit_block = False
    ratelimit_method = 'POST'



class InstagramDeleteView(DeleteMixIn):
    model = Instagram
    success_message = utils.DELETE_MESSAGE
## --------------------------------------------------------


@ratelimit(key='ip', rate='5/m')
def report_link(request, model_name, slug):
    # app_label is required to not conflict with other models
    content_type = ContentType.objects.get(model=model_name, app_label='links')
    model = content_type.model_class()
    obj = model.published.filter(slug=slug).first()

    # if object not exists or not published raise 403 error
    if obj is None:
        raise PermissionDenied

    initial = {
        'content_type': model_name,
        'object_id': obj.id,
        'url': obj.url,
    }

    if request.method == 'POST':
        form = ReportForm(request.POST, initial=initial)
        if form.is_valid():
            cd = form.cleaned_data
            text = cd.get('text')
            type = cd.get('type')
            email = cd.get('email')

            # create report
            report = Report.objects.create(
                email=email,
                type=type,
                text=text,
                content_object=obj,
                url=obj.url,
            )

            messages.success(request,
                _('Your report was successfully submitted.'))
            return redirect(reverse('links:index'))
        else:
            messages.error(request, utils.FAILED_FORM_SUBMISSION)
    else:
        form = ReportForm(initial=initial)

    context = {
        'object': obj,
        'form': form,
    }
    return render(request, 'links/report.html', context)


def tagged_items(request, tag_slug):
    """
    list all links that are tagged with `tag_slug`
    """
    tag_slug = unquote(tag_slug)
    tag = get_object_or_404(Tag, slug=tag_slug)
    websites = Website.published.filter(tags__in=[tag])
    channels = Channel.published.filter(tags__in=[tag])
    groups = Group.published.filter(tags__in=[tag])
    instagrams = Instagram.published.filter(tags__in=[tag])

    object_list = list(chain(websites, channels, groups, instagrams))

    # 20 links per page
    paginator = Paginator(object_list, utils.MAX_PAGE_LIMIT)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        'is_paginated': True,
        'page_obj': object_list,
        'tag': tag,
    }
    return render(request, 'links/tagged_items.html', context)


def search(request):
    q = request.GET.get('q')
    if q:
        query = (Q(title__icontains=q) | Q(description__icontains=q))

        # search the query in published links
        object_list = list(chain(
            Website.published.filter(query),
            Channel.published.filter(query),
            Group.published.filter(query),
            Instagram.published.filter(query))
        )
    else:
        object_list = None

    # 20 links per page
    paginator = Paginator(object_list, utils.MAX_PAGE_LIMIT)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        'is_paginated': True,
        'page_obj': object_list,
        'query_string': f'&q={q}', # search query
    }
    return render(request, 'links/search.html', context)


class CategoriesListView(ListView):
    model = Category


def categorized_items(request, category_id):
    """
    list all links that are categorized as category_id[name]
    """
    category = get_object_or_404(Category, pk=category_id)
    websites = Website.published.filter(category_id=category_id)
    channels = Channel.published.filter(category_id=category_id)
    groups = Group.published.filter(category_id=category_id)
    instagrams = Instagram.published.filter(category_id=category_id)

    object_list = list(chain(websites, channels, groups, instagrams))

    # 20 links per page
    paginator = Paginator(object_list, utils.MAX_PAGE_LIMIT)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {
        'is_paginated': True,
        'page_obj': object_list,
        'category': category,
    }
    return render(request, 'links/categorized_items.html', context)
