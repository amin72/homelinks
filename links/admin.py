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


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    list_editable = ('order',)


# Website
@admin.register(Website)
class WebsiteAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'type', 'title', 'status', 'url', 'category',
        'description', 'image')
    list_display = ('title', 'url', 'slug', 'status', 'author', 'category',
        'taggit_counter', 'is_parent')
    list_filter = ('type', 'status', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description', 'type')
    raw_id_fields = ('author', 'category')
    list_editable = ('status',)
    readonly_fields = ('parent',)
    inlines = [TaggitStackedInline]


# Channel
@admin.register(Channel)
class ChannelAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'application', 'channel_id',
        'category', 'description', 'image')
    list_display = ('title', 'channel_id', 'application', 'slug', 'status',
        'author', 'category', 'taggit_counter', 'is_parent')
    list_filter = ('application', 'status', 'created', 'updated', 'category')
    search_fields = ('title', 'channel_id', 'description')
    raw_id_fields = ('author', 'category')
    list_editable = ('status',)
    readonly_fields = ('application', 'parent')
    inlines = [TaggitStackedInline]


# Group
@admin.register(Group)
class GroupAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'url', 'application', 'category',
        'description', 'image')
    list_display = ('title', 'application', 'slug', 'status', 'author',
        'category', 'taggit_counter', 'is_parent')
    list_filter = ('application', 'status', 'created', 'updated', 'category')
    search_fields = ('title', 'url', 'description')
    raw_id_fields = ('author', 'category')
    list_editable = ('status',)
    readonly_fields = ('application', 'url', 'parent')
    inlines = [TaggitStackedInline]


# Instagram
@admin.register(Instagram)
class InstagramAdmin(TaggitCounter, admin.ModelAdmin):
    fields = ('author', 'title', 'status', 'page_id', 'category', 'description',
        'image')
    list_display = ('title', 'slug', 'status', 'author', 'page_id', 'category',
        'taggit_counter', 'is_parent')
    list_filter = ('created', 'status', 'updated', 'category')
    search_fields = ('title', 'page_id', 'description')
    raw_id_fields = ('author', 'category')
    list_editable = ('status',)
    readonly_fields = ('parent',)
    inlines = [TaggitStackedInline]

    def is_parent(self, obj):
        return obj.is_parent



# Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'email', 'url', 'type', 'is_read', 'created')
    list_filter = ('created', 'type', 'is_read')
    search_fields = ('email', 'text')
    list_editable = ('type', 'is_read')
