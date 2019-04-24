from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Action, User


# User
@admin.register(User)
class ProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
        'phone_number', 'is_premium', 'is_staff')
    list_editable = ('phone_number', 'is_premium')
    list_filter = ('is_staff', 'is_superuser', 'is_premium',)


# Action
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'type', 'is_read', 'is_child')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created')
    orderings = ('-updated',)
    readonly_fields = ['type', 'content_object', 'content_type', 'object_id']

    def is_child(self, obj):
        content_object = obj.content_object
        if hasattr(content_object, 'child'):
             return (content_object.parent is not None)
        return False
