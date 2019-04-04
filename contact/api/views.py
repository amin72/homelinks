from rest_framework.generics import CreateAPIView
from .serializers import ContactUsCreateSerializer


class ContactUsCreateAPIView(CreateAPIView):
	serializer_class = ContactUsCreateSerializer
