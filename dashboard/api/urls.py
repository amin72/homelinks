from django.urls import path, reverse_lazy
from . import views


app_name = 'dashboard-api'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.LinkListAPIView.as_view(), name='index'),

    # # rules
    # path('rules/', views.rules, name='rules'),
    #
    # # add-link
    # path('add_link/', views.add_link, name='add_link'),
    #
    # list user's websites
    path('users_websites/', views.UserWebsiteListAPIView.as_view(),
        name='users_websites'),

    # list user's channels
    path('users_channels/', views.UserChannelListAPIView.as_view(),
        name='users_channels'),

    # list user's groups
    path('users_groups/', views.UserGroupListAPIView.as_view(),
        name='users_groups'),

    # list user's instagrams
    path('users_instagrams/', views.UserInstagramListAPIView.as_view(),
        name='users_instagrams'),

    # user update
    path('user_update/', views.UserUpdateAPIView.as_view(), name='user_update'),
]
