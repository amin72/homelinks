from django.contrib import admin
from .models import Profile


# Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user', 'phone_number')
    raw_id_fields = ('user',)
    list_editable = ('phone_number',)
