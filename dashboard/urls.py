from django.contrib import admin
from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),

    # rules
    path('rules/', views.rules, name='rules'),

    # add-link
    path('add_link/', views.add_link, name='add_link'),

    # list user's channels
    path('users_channels/', views.UserChannelsListView.as_view(),
        name='users_channels'),

    # list user's groups
    path('users_groups/', views.UserGroupsListView.as_view(),
        name='users_groups'),

    # list user's instagrams
    path('users_instagrams/', views.UserInstagramsListView.as_view(),
        name='users_instagrams'),
]
