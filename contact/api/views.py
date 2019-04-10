from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import ContactUsCreateSerializer


class ContactUsCreateAPIView(CreateAPIView):
	serializer_class = ContactUsCreateSerializer
	permission_classes = [AllowAny]
