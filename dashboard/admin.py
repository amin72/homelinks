from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Action, User


# User
admin.site.register(User, UserAdmin)


# Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'vip')
    search_fields = ('user', 'phone_number')
    raw_id_fields = ('user',)
    list_editable = ('phone_number', 'vip')
    list_filter = ('vip',)


# Action
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'type', 'is_read', 'is_child')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created')
    orderings = ('-updated',)

    def is_child(self, obj):
        content_object = obj.content_object
        if hasattr(content_object, 'child'):
             return (content_object.parent is not None)
        return False
