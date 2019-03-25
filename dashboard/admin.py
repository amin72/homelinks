from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Profile, Action


# Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user', 'phone_number')
    raw_id_fields = ('user',)
    list_editable = ('phone_number',)


# Action
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'type', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created')
