from django.urls import path
from . import views


app_name = 'links-apis'

urlpatterns = [
    path('', views.IndexAPIView.as_view(), name='index'),

    # list websites
    path('websites/', views.WebsiteListAPIView.as_view(), name='websites'),

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
    path('<str:model_name>/<str:slug>/report_link/',
        views.ReportLinkAPIView.as_view(),
        name='report'),

    # # tagged items
    path('tag/<str:tag_slug>/', views.TaggedItemsAPIListView.as_view(),
        name='tagged_items'),

    # search
    path('search/', views.LinkSearchAPIView.as_view(), name='search'),

    # categories
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),

    # categorized items
    path('category/<int:category_id>/',
        views.CategorizedItemsAPIListView.as_view(),
        name='categorized_items'),
]
