from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as drf_views
from dashboard.api import views as dashboard_views


urlpatterns = i18n_patterns(
    # dashboard
    path('dashboard/', include('dashboard.urls')),

    # contact
    path('contact/', include('contact.urls')),

    # links
    path('', include('links.urls')),

    prefix_default_language=False
)

# admin
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    ### APIs ###
    # links-apis
    path('api/', include('links.api.urls')),

    # contact-apis
    path('api/contact/', include('contact.api.urls')),

    # dashboard-apis
    path('api/dashboard/', include('dashboard.api.urls')),

    # auth token
    path('api/auth/token/', drf_views.obtain_auth_token, name='auth_token'),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/register/', dashboard_views.UserRegisterAPIView.as_view(),
        name='register'),

    prefix_default_language=True
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
