from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # dashboard
    path('dashboard/', include('dashboard.urls')),

    # links
    path('', include('links.urls')),

    # APIs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
