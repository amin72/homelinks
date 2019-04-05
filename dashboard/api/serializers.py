from rest_framework import serializers
from links.models import Website, Channel, Group, Instagram
from links.api import serializers as link_serializers


class WebsiteSerializer(serializers.ModelSerializer):
    detail_url = link_serializers.WEBSITE_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
            'updated',
            'status',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class ChannelSerializer(serializers.ModelSerializer):
    detail_url = link_serializers.CHANNEL_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
            'updated',
            'status',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class GroupSerializer(serializers.ModelSerializer):
    detail_url = link_serializers.GROUP_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
            'updated',
            'status',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url



class InstagramSerializer(serializers.ModelSerializer):
    detail_url = link_serializers.INSTAGRAM_DETAIL_URL
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Instagram
        fields = [
            'title',
            'detail_url',
            'thumbnail',
            'created',
            'updated',
            'status',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url
