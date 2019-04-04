from rest_framework import serializers
from contact.models import ContactUs


class ContactUsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
            'email',
            'type',
            'text',
        ]
