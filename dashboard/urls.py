from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),

    # rules
    # path('rules/', views.rules, name='rules'),

    # add-link
    path('add_link/', views.add_link, name='add_link'),

    # list user's websites
    path('users_websites/', views.UserWebsiteListView.as_view(),
        name='users_websites'),

    # list user's channels
    path('users_channels/', views.UserChannelListView.as_view(),
        name='users_channels'),

    # list user's groups
    path('users_groups/', views.UserGroupListView.as_view(),
        name='users_groups'),

    # list user's instagrams
    path('users_instagrams/', views.UserInstagramListView.as_view(),
        name='users_instagrams'),

    # login user
    path('login/', auth_views.LoginView.as_view(
            template_name='dashboard/login.html',
            redirect_authenticated_user=True),
        name='login'),

    # register user
    path('register/', views.register, name='register'),

    # logout user
    path('logout/', auth_views.LogoutView.as_view(
        template_name='dashboard/logout.html'), name='logout'),

    # user update
    # path('user_update/', views.user_update, name='user_update'),
    path('user_update/', views.UserUpdateView.as_view(), name='user_update'),

    # change password urls
    path('password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='dashboard/password_change_form.html',
            success_url = reverse_lazy('dashboard:password_change_done')),
        name='password_change'),

    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='dashboard/password_change_done.html'),
        name='password_change_done'),

    # reset password urls
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('dashboard:password_reset_done')),
        name='password_reset'),

    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('dashboard:password_reset_complete')),
        name='password_reset_confirm'),

    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    path('recent_actions/', views.recent_actions, name='recent_actions'),

    path('hide_action/<int:pk>/', views.hide_action, name='hide_action'),
]
