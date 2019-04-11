from django.contrib.auth import get_user_model
from rest_framework import serializers
from links.models import Website, Channel, Group, Instagram
from links.api import utils
from dashboard.models import Profile


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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number']


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        profile = validated_data.get('profile')
        instance.profile.phone_number = profile.get('phone_number')
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]
