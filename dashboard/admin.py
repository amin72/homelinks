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
    list_display = ('content_object', 'type', 'is_read', 'get_url', 'get_admin_url')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created')

    def get_url(self, obj):
        obj_url = obj.content_object.url
        return obj_url
    get_url.admin_order_field = 'url'
    get_url.short_description = 'url'

    def get_admin_url(self, obj):
        return obj.content_object.get_admin_url()
    get_admin_url.short_description = 'admin url'
