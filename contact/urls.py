from django.urls import path
from . import views


app_name = 'contact'

urlpatterns = [
    # contact us
    path('contact_us/', views.contact_us, name='contact_us'),
]
