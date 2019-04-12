from rest_framework import serializers
from django.contrib.auth import get_user_model
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
from links import utils as links_utils
from dashboard.api.serializers import UserSerializer
from . import utils

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
#----------------------------------------------------------


class WebsiteSerializer(serializers.ModelSerializer):
    detail_url = utils.WEBSITE_DETAIL_URL
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
    author = UserSerializer()
    category = CategorySerializer()

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


class WebsiteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            'title',
            'url',
            'type',
            'category',
            'description',
            'image',
        ]

    def validate(self, data):
        instance = Website(**data)
        if links_utils.is_duplicate_url(instance):
            raise links_utils.serialize_validation_exceptions['website']
        return data


class WebsiteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            'title',
            'url',
            'type',
            'category',
            'description',
            'image',
        ]
#----------------------------------------------------------


class ChannelSerializer(serializers.ModelSerializer):
    detail_url = utils.CHANNEL_DETAIL_URL
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
    author = UserSerializer()
    category = CategorySerializer()

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


class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'application',
            'title',
            'channel_id',
            'category',
            'description',
            'image',
        ]

    def validate(self, data):
        instance = Channel(**data)

        if not links_utils.valid_channel_id(instance.channel_id,
                                            instance.application):
            raise serializers.ValidationError({'channel_id': INVALID_NAME})

        if not links_utils.valid_channel_length(instance.channel_id,
                                            instance.application):
            raise serializers.ValidationError({'channel_id': SHORT_NAME})

        instance.url = links_utils.generate_channel_url(instance.channel_id,
                                                instance.application)
        if links_utils.is_duplicate_url(instance):
            raise links_utils.serialize_validation_exceptions['channel']

        return data


class ChannelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'application',
            'title',
            'channel_id',
            'category',
            'description',
            'image',
        ]
#----------------------------------------------------------


class GroupSerializer(serializers.ModelSerializer):
    detail_url = utils.GROUP_DETAIL_URL
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
    author = UserSerializer()
    category = CategorySerializer()

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


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'application',
            'title',
            'url',
            'category',
            'description',
            'image',
        ]

    def validate(self, data):
        instance = Group(**data)
        if links_utils.is_duplicate_url(instance):
            raise links_utils.serialize_validation_exceptions['group']
        return data


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'application',
            'title',
            'url',
            'category',
            'description',
            'image',
        ]
#----------------------------------------------------------


class InstagramSerializer(serializers.ModelSerializer):
    detail_url = utils.INSTAGRAM_DETAIL_URL
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
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Instagram
        fields = [
            'title',
            'author',
            'url',
            'category',
            'created',
            'description',
            'image',
        ]


class InstagramCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagram
        fields = [
            'title',
            'page_id',
            'category',
            'description',
            'image',
        ]

    def validate(self, data):
        instance = Instagram(**data)
        if not links_utils.valid_instagram_id(instance.page_id):
            raise serializers.ValidationError({'page_id':
                                    links_utils.INSTAGRAM_ID_INCORRECT})

        instance.url = links_utils.generate_instagram_url(instance.page_id)
        if links_utils.is_duplicate_url(instance):
            raise links_utils.serialize_validation_exceptions['instagram']

        return data


class InstagramUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instagram
        fields = [
            'title',
            'page_id',
            'category',
            'description',
            'image',
        ]
#----------------------------------------------------------


class LinkReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'type',
            'email',
            'text',
        ]
