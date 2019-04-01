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
from links import utils

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
    view_name='links-apis:instagram-detail',
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
        if utils.is_duplicate_url(instance):
            raise serializers.ValidationError({'url':
                utils.WEBSITE_EXISTS})
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

        if not utils.valid_channel_id(instance.channel_id,
                                        instance.application):
            raise serializers.ValidationError({'channel_id':
                _('Sorry, this name is invalid')})

        if not utils.valid_channel_length(instance.channel_id,
                                        instance.application):
            raise serializers.ValidationError({'channel_id':
                _(f'Sorry, This name is too short')})

        instance.url = utils.generate_channel_url(instance.channel_id,
                                                instance.application)
        if utils.is_duplicate_url(instance):
            raise serializers.ValidationError({'channel_id':
                utils.CHANNEL_EXISTS})

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
        if utils.is_duplicate_url(instance):
            raise serializers.ValidationError({'url':
                utils.GROUP_EXISTS})
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
        if not utils.valid_instagram_id(instance.page_id):
            raise serializers.ValidationError({'page_id':
                _('Your Instagram id is incorrect')})

        instance.url = utils.generate_instagram_url(instance.page_id)
        if utils.is_duplicate_url(instance):
            raise serializers.ValidationError({'page_id':
                utils.INSTAGRAM_EXISTS})

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
