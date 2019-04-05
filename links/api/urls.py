from django.urls import path
from . import views


app_name = 'links-apis'

urlpatterns = [
    path('', views.index, name='index'),

    # list websites
    path('websites/', views.WebsiteListAPIView.as_view(), name='websites'),

    # list iranian websites
    path('websites/iranian/', views.IranianWebsiteListAPIView.as_view(),
        name='iranian-websites'),

    # list foreign websites
    path('websites/foreign/', views.ForeignWebsiteListAPIView.as_view(),
        name='foreign-websites'),

    # website create
    path('websites/create/', views.WebsiteCreateAPIView.as_view(),
       name='website-create'),

    # website details
    path('website/<slug:slug>/', views.WebsiteDetailAPIView.as_view(),
        name='website-detail'),

    # website update
    path('website/<slug:slug>/update/', views.WebsiteUpdateAPIView.as_view(),
        name='website-update'),

    # website delete
    path('website/<slug:slug>/delete/', views.WebsiteDeleteAPIView.as_view(),
        name='website-delete'),

    # list channels
    path('channels/', views.ChannelListAPIView.as_view(), name='channels'),

    # list telegram channels
    path('channels/telegram/', views.TelegramChannelListAPIView.as_view(),
        name='telegram-channels'),

    # list soroush channels
    path('channels/soroush/', views.SoroushChannelListAPIView.as_view(),
        name='soroush-channels'),

    # list gap channels
    path('channels/gap/', views.GapChannelListAPIView.as_view(),
        name='gap-channels'),

    # list igap channels
    path('channels/igap/', views.IGapChannelListAPIView.as_view(),
        name='igap-channels'),

    # list eitaa channels
    path('channels/eitaa/', views.EitaaChannelListAPIView.as_view(),
        name='eitaa-channels'),

    # channel create
    path('channels/create/', views.ChannelCreateAPIView.as_view(),
       name='channel-create'),

    # channel details
    path('channel/<slug:slug>/', views.ChannelDetailAPIView.as_view(),
        name='channel-detail'),

    # channel update
    path('channel/<slug:slug>/update/', views.ChannelUpdateAPIView.as_view(),
        name='channel-update'),

    # channel delete
    path('channel/<slug:slug>/delete/', views.ChannelDeleteAPIView.as_view(),
        name='channel-delete'),

    # list groups
    path('groups/', views.GroupListAPIView.as_view(), name='groups'),

    # list whatsapp groups
    path('groups/whatsapp/', views.WhatsappGroupListAPIView.as_view(),
        name='whatsapp-groups'),

    # list telegram groups
    path('groups/telegram/', views.TelegramGroupListAPIView.as_view(),
        name='telegram-groups'),

    # list soroush groups
    path('groups/soroush/', views.SoroushGroupListAPIView.as_view(),
        name='soroush-groups'),

    # list gap groups
    path('groups/gap/', views.GapGroupListAPIView.as_view(),
        name='gap-groups'),

    # list igap groups
    path('groups/igap/', views.IGapGroupListAPIView.as_view(),
        name='igap-groups'),

    # list eitaa groups
    path('groups/eitaa/', views.EitaaGroupListAPIView.as_view(),
        name='eitaa-groups'),

    # group create
    path('groups/create/', views.GroupCreateAPIView.as_view(),
       name='group-create'),

    # group details
    path('group/<str:slug>/', views.GroupDetailAPIView.as_view(),
        name='group-detail'),

    # group update
    path('group/<str:slug>/update/', views.GroupUpdateAPIView.as_view(),
        name='group-update'),

    # group delete
    path('group/<str:slug>/delete/', views.GroupDeleteAPIView.as_view(),
        name='group-delete'),

    # list instagrams
    path('instagrams/', views.InstagramListAPIView.as_view(),
        name='instagrams'),

    # instagram create
    path('instagrams/create/', views.InstagramCreateAPIView.as_view(),
       name='instagram-create'),

    # instagram details
    path('instagram/<slug:slug>/', views.InstagramDetailAPIView.as_view(),
        name='instagram-detail'),

    # instagram update
    path('instagram/<slug:slug>/update/', views.InstagramUpdateAPIView.as_view(),
        name='instagram-update'),

    # instagram delete
    path('instagram/<slug:slug>/delete/',
        views.InstagramDeleteAPIView.as_view(),
        name='instagram-delete'),

    # report link
    path('report/<str:model_name>/<str:slug>/',
        views.ReportLinkAPIView.as_view(),
        name='report'),

    # # tagged items
    # path('tag/<str:tag_slug>/', views.tagged_items, name='tagged_items'),
    #
    # # search
    # path('search/', views.search, name='search'),
]
