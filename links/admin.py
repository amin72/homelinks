from django.contrib import admin
from .models import Category, Website, Channel, Group, Instagram


# CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


# WEBSITE
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'url', 'category', 'description',
        'image', 'tags', 'parent')
    list_display = ('title', 'url', 'slug', 'status', 'author', 'category',
        'created')
    list_filter = ('type', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description', 'type')
    raw_id_fields = ('author', 'category')


# CHANNEL
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'application', 'channel_id', 'category', 'description',
        'image', 'tags', 'parent')
    list_display = ('title', 'channel_id', 'application', 'slug', 'status', 'category',
        'created')
    list_filter = ('application', 'created', 'updated', 'category')
    search_fields = ('title', 'channel_id', 'description')
    raw_id_fields = ('author', 'category')


# GROUP
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'url', 'application', 'category', 'description',
        'image', 'tags', 'parent')
    list_display = ('title', 'status', 'slug', 'application', 'author',
        'category', 'created')
    list_filter = ('application', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description')
    raw_id_fields = ('author', 'category')


# INSTAGRAM
@admin.register(Instagram)
class InstagramAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'slug', 'page_id', 'author', 'category',
        'created')
    list_filter = ('created', 'updated', 'category')
    search_fields = ('title', 'slug', 'page_id', 'description')
    prepopulated_fields = {'slug': ('page_id',)}
    raw_id_fields = ('author', 'category')
