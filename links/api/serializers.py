from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from links import utils
from links.models import (
    Category,
    Website,
    Channel,
    Group,
    Instagram,
    Report,
)


User = get_user_model()


# url details
WEBSITE_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:website-detail',
    lookup_field='slug',
)

CHANNEL_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:channel-detail',
    lookup_field='slug',
)

GROUP_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:group-detail',
    lookup_field='slug',
)

INSTAGRAM_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:group-detail',
    lookup_field='slug',
)
#----------------------------------------------------------


class WebsiteListSerializer(serializers.ModelSerializer):
    detail_url = WEBSITE_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class WebsiteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            'title',
            'author',
            'url',
            'type',
            'category',
            'created',
            'description',
            'image',
        ]
#----------------------------------------------------------


class ChannelListSerializer(serializers.ModelSerializer):
    detail_url = CHANNEL_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created'
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class ChannelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'title',
            'author',
            'url',
            'application',
            'category',
            'created',
            'description',
            'image',
        ]
#----------------------------------------------------------


class GroupListSerializer(serializers.ModelSerializer):
    detail_url = GROUP_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'title',
            'author',
            'url',
            'application',
            'category',
            'created',
            'description',
            'image',
        ]
#----------------------------------------------------------

class InstagramListSerializer(serializers.ModelSerializer):
    detail_url = INSTAGRAM_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Instagram
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class InstagramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'title',
            'author',
            'url',
            'category',
            'created',
            'description',
            'image',
        ]
#----------------------------------------------------------

