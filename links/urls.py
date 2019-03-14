from django.contrib import admin
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

    # website details
    path('website/<slug:slug>/', views.WebsiteDetailView.as_view(),
        name='website-detail'),

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
    path('channels/<slug:slug>/', views.ChannelDetailView.as_view(),
        name='channel-detail'),

    # channel update
    path('channels/<slug:slug>/update/', views.ChannelUpdateView.as_view(),
        name='channel-update'),

    # channel delete
    path('channels/<slug:slug>/delete/', views.ChannelDeleteView.as_view(),
        name='channel-delete'),
]
