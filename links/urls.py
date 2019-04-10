from django.urls import path
from . import views


app_name = 'links'

urlpatterns = [
    path('', views.index, name='index'),

    # list websites
    path('websites/', views.WebsiteListView.as_view(), name='websites'),

    # list iranian websites
    path('websites/iranian/', views.IranianWebsiteListView.as_view(),
        name='iranian-websites'),

    # list foreign websites
    path('websites/foreign/', views.ForeignWebsiteListView.as_view(),
        name='foreign-websites'),

    # website create
    path('websites/create/', views.WebsiteCreateView.as_view(),
        name='website-create'),

    # website delete
    path('website/<slug:slug>/', views.WebsiteDetailView.as_view(),
        name='website-detail'),

    # website update
    path('website/<slug:slug>/update/', views.WebsiteUpdateView.as_view(),
        name='website-update'),

    # website delete
    path('website/<slug:slug>/delete/', views.WebsiteDeleteView.as_view(),
        name='website-delete'),

    # list channels
    path('channels/', views.ChannelListView.as_view(), name='channels'),

    # list telegram channels
    path('channels/telegram/', views.TelegramChannelListView.as_view(),
        name='telegram-channels'),

    # list soroush channels
    path('channels/soroush/', views.SoroushChannelListView.as_view(),
        name='soroush-channels'),

    # list gap channels
    path('channels/gap/', views.GapChannelListView.as_view(),
        name='gap-channels'),

    # list igap channels
    path('channels/igap/', views.IGapChannelListView.as_view(),
        name='igap-channels'),

    # list eitaa channels
    path('channels/eitaa/', views.EitaaChannelListView.as_view(),
        name='eitaa-channels'),

    # channel create
    path('channels/create/', views.ChannelCreateView.as_view(),
        name='channel-create'),

    # channel details
    path('channel/<slug:slug>/', views.ChannelDetailView.as_view(),
        name='channel-detail'),

    # channel update
    path('channel/<slug:slug>/update/', views.ChannelUpdateView.as_view(),
        name='channel-update'),

    # channel delete
    path('channel/<slug:slug>/delete/', views.ChannelDeleteView.as_view(),
        name='channel-delete'),

    # list groups
    path('groups/', views.GroupListView.as_view(), name='groups'),

    # list whatsapp groups
    path('groups/whatsapp/', views.WhatsappGroupListView.as_view(),
        name='whatsapp-groups'),

    # list telegram groups
    path('groups/telegram/', views.TelegramGroupListView.as_view(),
        name='telegram-groups'),

    # list soroush groups
    path('groups/soroush/', views.SoroushGroupListView.as_view(),
        name='soroush-groups'),

    # list gap groups
    path('groups/gap/', views.GapGroupListView.as_view(),
        name='gap-groups'),

    # list igap groups
    path('groups/igap/', views.IGapGroupListView.as_view(),
        name='igap-groups'),

    # list eitaa groups
    path('groups/eitaa/', views.EitaaGroupListView.as_view(),
        name='eitaa-groups'),

    # group create
    path('groups/create/', views.GroupCreateView.as_view(), name='group-create'),

    # group details
    path('group/<str:slug>/', views.GroupDetailView.as_view(),
        name='group-detail'),

    # group update
    path('group/<str:slug>/update/', views.GroupUpdateView.as_view(),
        name='group-update'),

    # group delete
    path('group/<str:slug>/delete/', views.GroupDeleteView.as_view(),
        name='group-delete'),

    # list instagrams
    path('instagrams/', views.InstagramListView.as_view(), name='instagrams'),

    # instagram create
    path('instagrams/create/', views.InstagramCreateView.as_view(),
        name='instagram-create'),

    # instagram details
    path('instagram/<slug:slug>/', views.InstagramDetailView.as_view(),
        name='instagram-detail'),

    # instagram update
    path('instagram/<slug:slug>/update/', views.InstagramUpdateView.as_view(),
        name='instagram-update'),

    # instagram delete
    path('instagram/<slug:slug>/delete/', views.InstagramDeleteView.as_view(),
        name='instagram-delete'),

    # report link
    path('<str:model_name>/<str:slug>/report/', views.report_link,
        name='report'),

    # tagged items
    path('tag/<str:tag_slug>/', views.tagged_items, name='tagged_items'),

    # search
    path('search/', views.search, name='search'),
]
