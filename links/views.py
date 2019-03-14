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
    DetailMixIn,
    ApplicationMixIn,
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



# list all posts: websites, channels, groups, and instagrams
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
        return Website.objects.filter(visible=True, type='iranian')


# list foreign websites
class ForeignWebsiteListView(ListView):
    """List all published and foreign websites"""
    def get_queryset(self):
        return Website.objects.filter(visible=True, type='foreign')


# website detail
class WebsiteDetailView(DetailMixIn):
    model = Website
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
class ChannelDetailView(DetailMixIn):
    model = Channel


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
