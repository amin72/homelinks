from django.contrib import admin
from .models import ContactUs


# ContactUs
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'is_read')
    search_fields = ('email', 'type', 'text')
    list_editable = ('type', 'is_read')
    readonly_fields = ('email', 'text',)
