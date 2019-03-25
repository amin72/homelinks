from itertools import chain

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext, ugettext as _
from django.contrib import messages
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from .models import (
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
from dashboard.models import Action


## ------- MESSAGES -------------------------------------------------
create_message = _('Your link was successfully created. And it will be '
                   'processed and published in 24 hours.')

update_message = _('Your link was successfully updated. And it will be '
                   'processed and published in 24 hours.')

delete_message = _('Your link was successfully deleted.')
## ------------------------------------------------------------------



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


# list websites
class WebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published websites"""
    model_name = 'website'
    queryset = Website.published.all()


# list iranian websites
class IranianWebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published and iranian websites"""
    model_name = 'website'

    def get_queryset(self):
        return Website.published.filter(type='iranian')


# list foreign websites
class ForeignWebsiteListView(SetActiveCssClassMixIn, ListView):
    """List all published and foreign websites"""
    model_name = 'website'

    def get_queryset(self):
        return Website.published.filter(type='foreign')


# website detail
class WebsiteDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    """
    Give detail about published object
    """
    model = Website
    lookup_field = 'slug'
    model_name = 'website'


# website create
class WebsiteCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Website
    form_class = CreateWebsiteForm
    success_message = create_message


# website update
class WebsiteUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Website
    success_message = update_message
    fields = (
        'title',
        'url',
        'type',
        'category',
        'description',
        'image'
    )


# website delete
class WebsiteDeleteView(DeleteMixIn):
    model = Website
    success_message = delete_message
## -----------------------------------------------------


# list channels
class ChannelListView(SetActiveCssClassMixIn, ListView):
    queryset = Channel.published.all().filter(parent=None)
    model_name = 'channel'


# list telegram channels
class TelegramChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='telegram'
    model_name = 'channel'


# list soroush channels
class SoroushChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='soroush'
    model_name = 'channel'


# list gap channels
class GapChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='gap'
    model_name = 'channel'


# list igap channels
class IGapChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='igap'
    model_name = 'channel'


# list eitaa channels
class EitaaChannelListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Channel
    application='eitaa'
    model_name = 'channel'


# channel details
class ChannelDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Channel
    lookup_field = 'slug'
    model_name = 'channel'


# channel create
class ChannelCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Channel
    form_class = CreateChannelForm
    success_message = create_message


# channel update
class ChannelUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Channel
    success_message = update_message
    fields = (
        'application',
        'title',
        'channel_id',
        'category',
        'description',
        'image'
    )


# channel delete
class ChannelDeleteView(DeleteMixIn):
    model = Channel
    success_message = delete_message
## -----------------------------------------------------


# list groups
class GroupListView(SetActiveCssClassMixIn, ListView):
    queryset = Group.published.all()
    model_name = 'group'


# list whatsapp groups
class WhatsappGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application = 'whatsapp'
    model_name = 'group'


# list telegram groups
class TelegramGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='telegram'
    model_name = 'group'


# list soroush groups
class SoroushGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='soroush'
    model_name = 'group'


# list gap groups
class GapGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='gap'
    model_name = 'group'


# list igap groups
class IGapGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='igap'
    model_name = 'group'


# list eitaa groups
class EitaaGroupListView(SetActiveCssClassMixIn, ApplicationMixIn):
    model = Group
    application='eitaa'
    model_name = 'group'


# group detail
class GroupDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Group
    lookup_field = 'slug'
    model_name = 'group'


# group create
class GroupCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Group
    form_class = CreateGroupForm
    success_message = create_message


# group update
class GroupUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Group
    fields = (
        'application',
        'title',
        'url',
        'category',
        'description',
        'image'
    )
    success_message = update_message


# group delete
class GroupDeleteView(DeleteMixIn):
    model = Group
    success_message = delete_message
## -----------------------------------------------------


# list instagrams
class InstagramListView(SetActiveCssClassMixIn, ListView):
    queryset = Instagram.published.all()
    model_name = 'instagram'


# instagram details
class InstagramDetailView(PublishedObjectMixIn, SetModelNameMixIn, DetailView):
    model = Instagram
    lookup_field = 'slug'
    model_name = 'instagram'


# instagram create
class InstagramCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Instagram
    form_class = CreateInstagramForm
    success_message = create_message


# instagram update
class InstagramUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Instagram
    fields = (
        'title',
        'page_id',
        'category',
        'description',
        'image'
    )
    success_message = update_message


# instagram delete
class InstagramDeleteView(DeleteMixIn):
    model = Instagram
    success_message = delete_message
## --------------------------------------------------------


# Report links
def report_link(request, model_name, slug):
    # app_label is required to not conflict with other models
    content_type = ContentType.objects.get(model=model_name, app_label='links')
    model = content_type.model_class()
    object = model.published.get(slug=slug)
    url = object.url

    initial = {
        'content_type': model_name,
        'object_slug': slug,
        'url': url,
    }

    if request.method == 'POST':
        form = ReportForm(request.POST, initial=initial)
        if form.is_valid():
            cd = form.cleaned_data
            c_type = cd.get('content_type')
            object_slug = cd.get('object_slug')
            text = cd.get('text')
            type = cd.get('type')
            email = cd.get('email')

            # create report
            report = Report.objects.create(
                email=email,
                type=type,
                text=text,
                content_type=content_type,
                object_slug=object_slug,
                url=url,
            )

            # create action for the report
            model_name = Report.__name__.lower()
            content_type = ContentType.objects.get(model=model_name,
                app_label='links')
            Action.objects.get_or_create(type='report created',
                content_type=content_type, object_id=report.id)

            messages.success(request,
                _('Your report was successfully submitted.'))
            return redirect(reverse('links:index'))
        else:
            error_message = "Something went wrong. Fill all fields and try again."
            messages.error(request, _(error_message))
    else:
        form = ReportForm(initial=initial)

    context = {
        'object': object,
        'form': form,
    }
    return render(request, 'links/report.html', context)


def tagged_items(request, tag_slug=None):
    """
    list all links that are tagged with `tag_slug`
    """
    websites = Website.published.all()
    channels = Channel.published.all()
    groups = Group.published.all()
    instagrams = Instagram.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        websites = websites.filter(tags__in=[tag])
        channels = channels.filter(tags__in=[tag])
        groups = groups.filter(tags__in=[tag])
        instagrams = instagrams.filter(tags__in=[tag])

    context = {
        'websites': websites,
        'channels': channels,
        'groups': groups,
        'instagrams': instagrams,
    }

    object_list = list(chain(websites, channels, groups, instagrams))

    paginator = Paginator(object_list, 20) # 20 links per page
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render(request, 'links/tagged_items.html',
        {'page': page, 'object_list': object_list, 'tag': tag})


# search
def search(request):
    q = request.GET.get('q')
    if q:
        query = (Q(title__icontains=q) | Q(description__icontains=q))

        # search the query in published links
        search_result = chain(
            Website.published.filter(query),
            Channel.published.filter(query),
            Group.published.filter(query),
            Instagram.published.filter(query))
    else:
        search_result = None

    return render(request, 'links/search.html', {
        'search_result': search_result})
