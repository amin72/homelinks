from django.contrib.auth import get_user_model
from rest_framework import serializers
from links.models import Website, Channel, Group, Instagram
from links.api import utils


User = get_user_model()


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
            'updated',
            'status',
        ]

    def get_thumbnail(self, obj):
        return obj.thumbnail_url


class ChannelSerializer(serializers.ModelSerializer):
    detail_url = utils.CHANNEL_DETAIL_URL
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
    detail_url = utils.GROUP_DETAIL_URL
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
    detail_url = utils.INSTAGRAM_DETAIL_URL
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


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, data):
        """
        Check if new_password1 and new_password2 are the same
        """
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                {'new_password1': 'New Passwords do not match'})
        else:
            return data
