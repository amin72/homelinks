from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # dashboard
    path('dashboard/', include('dashboard.urls')),

    # contact
    path('contact/', include('contact.urls')),

    # links
    path('', include('links.urls')),

    ### APIs ###
    # links-apis
    path('api/', include('links.api.urls')),

    # contact-apis
    path('api/contact/', include('contact.api.urls')),

    # dashboard-apis
    # path('api/dashboard/', include('dashboard.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
