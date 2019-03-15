from django.shortcuts import render
from django.utils.translation import gettext, ugettext as _
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)
from .models import Website, Channel, Group, Instagram
from .mixins import (
    ApplicationMixIn,
    PublishedObjectMixIn,
    LoginRequiredMixin,
    InfoMessageMixin,
    CreateMixIn,
    OwnerMixin,
    UpdateMixIn,
    DeleteMixIn,
)


## ------- MESSAGES -------------------------------------------------
create_message = _('Your link was successfully created. And it will be '
                   'processed and published in 24 hours.')

update_message = _('Your Link was successfully updated. And it will be '
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
    }
    return render(request, 'links/index.html', context)


# list websites
class WebsiteListView(ListView):
    """List all published websites"""
    queryset = Website.published.all()


# list iranian websites
class IranianWebsiteListView(ListView):
    """List all published and iranian websites"""
    def get_queryset(self):
        return Website.published.filter(type='iranian')


# list foreign websites
class ForeignWebsiteListView(ListView):
    """List all published and foreign websites"""
    def get_queryset(self):
        return Website.published.filter(type='foreign')


# website detail
class WebsiteDetailView(PublishedObjectMixIn, DetailView):
    """
    Give detail about published object
    """
    model = Website
    lookup_field = 'slug'
## -----------------------------------------------------



# list channels
class ChannelListView(ListView):
    queryset = Channel.published.all()


# list telegram channels
class TelegramChannelListView(ApplicationMixIn):
    model = Channel
    application='telegram'


# list soroush channels
class SoroushChannelListView(ApplicationMixIn):
    model = Channel
    application='soroush'


# list gap channels
class GapChannelListView(ApplicationMixIn):
    model = Channel
    application='gap'


# list igap channels
class IGapChannelListView(ApplicationMixIn):
    model = Channel
    application='igap'


# list eitaa channels
class EitaaChannelListView(ApplicationMixIn):
    model = Channel
    application='eitaa'


# channel details
class ChannelDetailView(PublishedObjectMixIn, DetailView):
    model = Channel
    lookup_field = 'slug'


# channel create
class ChannelCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Channel
    fields = (
        'application',
        'title',
        'channel_id',
        'category',
        'description',
        'image'
    )
    success_message = create_message


# channel update
class ChannelUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Channel
    fields = (
        'application',
        'title',
        'channel_id',
        'category',
        'description',
        'image'
    )
    success_message = update_message


# channel delete
class ChannelDeleteView(DeleteMixIn):
    model = Channel
    success_message = delete_message
## -----------------------------------------------------


# list groups
class GroupListView(ListView):
    queryset = Group.published.all()


# list whatsapp groups
class WhatsappGroupListView(ApplicationMixIn):
    model = Group
    application = 'whatsapp'


# list telegram groups
class TelegramGroupListView(ApplicationMixIn):
    model = Group
    application='telegram'


# list soroush groups
class SoroushGroupListView(ApplicationMixIn):
    model = Group
    application='soroush'


# list gap groups
class GapGroupListView(ApplicationMixIn):
    model = Group
    application='gap'


# list igap groups
class IGapGroupListView(ApplicationMixIn):
    model = Group
    application='igap'


# list eitaa groups
class EitaaGroupListView(ApplicationMixIn):
    model = Group
    application='eitaa'


# group detail
class GroupDetailView(PublishedObjectMixIn, DetailView):
    model = Group
    lookup_field = 'slug'


# group create
class GroupCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Group
    fields = (
        'application',
        'title',
        'link',
        'category',
        'description',
        'image'
    )
    success_message = create_message


# group update
class GroupUpdateView(LoginRequiredMixin, OwnerMixin, UpdateMixIn):
    model = Group
    fields = (
        'application',
        'title',
        'link',
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
class InstagramListView(ListView):
    queryset = Instagram.published.all()


# instagram details
class InstagramDetailView(PublishedObjectMixIn, DetailView):
    model = Instagram
    lookup_field = 'slug'


# instagram create
class InstagramCreateView(LoginRequiredMixin, InfoMessageMixin, CreateMixIn):
    model = Instagram
    fields = (
        'title',
        'page_id',
        'category',
        'description',
        'image'
    )
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
