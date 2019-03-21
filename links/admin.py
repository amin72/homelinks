from django.contrib import admin
from taggit.models import Tag
from taggit_helpers.admin import (
    TaggitCounter,
    TaggitStackedInline,
    TaggitTabularInline,
)
from .models import (
    Category,
    Website,
    Channel,
    Group,
    Instagram,
    Report
)


# CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


# WEBSITE
@admin.register(Website)
class WebsiteAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'type', 'title', 'status', 'url', 'category',
        'description', 'image', 'parent')
    list_display = ('title', 'url', 'slug', 'status', 'author', 'category',
        'created', 'taggit_counter',)
    list_filter = ('type', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description', 'type')
    raw_id_fields = ('author', 'category')
    list_editable = ('status', 'created')
    inlines = [TaggitStackedInline]


# CHANNEL
@admin.register(Channel)
class ChannelAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'application', 'channel_id',
        'category', 'description', 'image', 'parent')
    list_display = ('title', 'channel_id', 'application', 'slug', 'status',
        'category', 'created', 'taggit_counter',)
    list_filter = ('application', 'created', 'updated', 'category')
    search_fields = ('title', 'channel_id', 'description')
    raw_id_fields = ('author', 'category')
    list_editable = ('status', 'created')
    inlines = [TaggitStackedInline]


# GROUP
@admin.register(Group)
class GroupAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'url', 'application', 'category', 'description',
        'image', 'tags', 'parent')
    list_display = ('title', 'status', 'slug', 'application', 'author',
        'category', 'created', 'taggit_counter')
    list_filter = ('application', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description')
    raw_id_fields = ('author', 'category')
    list_editable = ('status', 'created')
    inlines = [TaggitStackedInline]


# INSTAGRAM
@admin.register(Instagram)
class InstagramAdmin(TaggitCounter, admin.ModelAdmin):
    list_display = ('title', 'status', 'slug', 'page_id', 'author', 'category',
        'created', 'taggit_counter')
    list_filter = ('created', 'updated', 'category')
    search_fields = ('title', 'slug', 'page_id', 'description')
    prepopulated_fields = {'slug': ('page_id',)}
    raw_id_fields = ('author', 'category')
    list_editable = ('status', 'created')
    inlines = [TaggitStackedInline]


# LINK_REPORT
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('email', 'url', 'type', 'is_read', 'created')
    list_filter = ('created', 'type', 'is_read')
    search_fields = ('email', 'text')
    list_editable = ('type', 'is_read')
