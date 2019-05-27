from django.urls import path
from . import views


app_name = 'links'

urlpatterns = [
    path('', views.index, name='index'),

    # list websites
    path('websites/', views.WebsiteListView.as_view(), name='websites'),

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
    path('<str:model_name>/<str:slug>/report_link/', views.report_link,
        name='report'),

    # tagged items
    path('tag/<str:tag_slug>/', views.tagged_items, name='tagged_items'),

    # search
    path('search/', views.search, name='search'),

    # categories
    path('categories/', views.CategoriesListView.as_view(), name='categories'),

    # categorized items
    path('category/<int:category_id>/', views.categorized_items,
        name='categorized_items'),
]
