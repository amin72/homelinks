from django.urls import path
from . import views


app_name = 'contact-apis'

urlpatterns = [
    # contact us
    path('contact_us/', views.ContactUsCreateAPIView.as_view(),
        name='contact_us'),
]
