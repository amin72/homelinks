from itertools import chain

from django.db.models import Q
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	UpdateAPIView,
)

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
)

from links.models import (
    Category,
    Website,
    Channel,
    Group,
    Instagram,
    Report,
)

from .serializers import (
	WebsiteSerializer,
	WebsiteDetailSerializer,
	WebsiteCreateSerializer,
	WebsiteUpdateSerializer,

	ChannelSerializer,
	ChannelDetailSerializer,
	ChannelCreateSerializer,
	ChannelUpdateSerializer,

	GroupSerializer,
	GroupDetailSerializer,
	GroupCreateSerializer,
	GroupUpdateSerializer,

	InstagramSerializer,
	InstagramDetailSerializer,
	InstagramCreateSerializer,
	InstagramUpdateSerializer,

	LinkReportSerializer,
	CategorySerializer,
)

from links.mixins import (
	CreateAPIMixIn,
	RetrieveUpdateAPIMixIn,
	DeleteAPIMixIn,
)

from links import utils
from .pagination import LinkPageNumberPagination
from .permissions import IsPremiumUser, IsOwner


class IndexAPIView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		websites = Website.published.all()[:6]
		channels = Channel.published.all()[:6]
		groups = Group.published.all()[:6]
		instagrams = Instagram.published.all()[:6]

		serialized_websites = WebsiteSerializer(websites, many=True,
			context={'request': request})
		serialized_channels = ChannelSerializer(channels, many=True,
			context={'request': request})
		serialized_groups = GroupSerializer(groups, many=True,
			context={'request': request})
		serialized_instagrams = InstagramSerializer(instagrams, many=True,
			context={'request': request})

		result = {
			'websites': serialized_websites.data,
			'channels': serialized_channels.data,
			'groups': serialized_groups.data,
			'instagram': serialized_instagrams.data,
		}
		return Response(result)


class WebsiteListAPIView(ListAPIView):
	serializer_class = WebsiteSerializer
	queryset = Website.published.all()
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class IranianWebsiteListAPIView(ListAPIView):
	serializer_class = WebsiteSerializer
	queryset = Website.published.filter(type='iranian')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class ForeignWebsiteListAPIView(ListAPIView):
	serializer_class = WebsiteSerializer
	queryset = Website.published.filter(type='foreign')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class WebsiteDetailAPIView(RetrieveAPIView):
	serializer_class = WebsiteDetailSerializer
	queryset = Website.published.all()
	lookup_field = 'slug'
	permission_classes = [AllowAny]


class WebsiteCreateAPIView(CreateAPIMixIn):
	serializer_class = WebsiteCreateSerializer
	# only premium users can add websites
	permission_classes = [IsAuthenticated, IsPremiumUser]


class WebsiteUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = WebsiteUpdateSerializer
	queryset = Website.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Website


class WebsiteDeleteAPIView(DeleteAPIMixIn):
	queryset = Website.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Website
#----------------------------------------------------------


class ChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.all()
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class TelegramChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.filter(application='telegram')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class SoroushChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.filter(application='soroush')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class GapChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.filter(application='gap')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class IGapChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.filter(application='igap')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class EitaaChannelListAPIView(ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.filter(application='eitaa')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class ChannelDetailAPIView(RetrieveAPIView):
	serializer_class = ChannelDetailSerializer
	queryset = Channel.published.all()
	lookup_field = 'slug'
	permission_classes = [AllowAny]


class ChannelCreateAPIView(CreateAPIMixIn):
	serializer_class = ChannelCreateSerializer


class ChannelUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = ChannelUpdateSerializer
	queryset = Channel.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Channel


class ChannelDeleteAPIView(DestroyAPIView):
	queryset = Channel.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
# ---------------------------------------------------------


class GroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.all()
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class WhatsappGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='whatsapp')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class TelegramGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='telegram')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class SoroushGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='soroush')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class GapGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='gap')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class IGapGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='igap')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class EitaaGroupListAPIView(ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.filter(application='eitaa')
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class GroupDetailAPIView(RetrieveAPIView):
	serializer_class = GroupDetailSerializer
	queryset = Group.published.all()
	lookup_field = 'slug'
	permission_classes = [AllowAny]


class GroupCreateAPIView(CreateAPIMixIn):
	serializer_class = GroupCreateSerializer


class GroupUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = GroupUpdateSerializer
	queryset = Group.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Group


class GroupDeleteAPIView(DestroyAPIView):
	queryset = Group.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
# --------------------------------------------------------


class InstagramListAPIView(ListAPIView):
	serializer_class = InstagramSerializer
	queryset = Instagram.published.all()
	pagination_class = LinkPageNumberPagination
	permission_classes = [AllowAny]


class InstagramDetailAPIView(RetrieveAPIView):
	serializer_class = InstagramDetailSerializer
	queryset = Instagram.published.all()
	lookup_field = 'slug'
	permission_classes = [AllowAny]


class InstagramCreateAPIView(CreateAPIMixIn):
	serializer_class = InstagramCreateSerializer


class InstagramUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = InstagramUpdateSerializer
	queryset = Instagram.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Instagram


class InstagramDeleteAPIView(DeleteAPIMixIn):
	queryset = Instagram.published.all()
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	model = Instagram
# ---------------------------------------------------------


class ReportLinkAPIView(CreateAPIView):
	serializer_class = LinkReportSerializer
	permission_classes = [AllowAny]

	def perform_create(self, serializer):
		model_name = self.kwargs.get('model_name')
		slug = self.kwargs.get('slug')

		content_type = ContentType.objects.get(model=model_name,
			app_label='links')
		model = content_type.model_class()
		obj = model.published.filter(slug=slug).first()
		if obj is None:
			raise Http404
		data = serializer.data

		report = Report.objects.create(
            email=data.get('email'),
            type=data.get('type'),
            text=data.get('text'),
            content_object=obj,
            url=obj.url,
        )

		return serializer


class LinkSearchAPIView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		q = request.GET.get('q')
		if q:
		    query = (Q(title__icontains=q) | Q(description__icontains=q))

		    # search the query in published links
		    search_result = chain(
		        WebsiteSerializer(
					Website.published.filter(query),
					many=True,
					context={'request': request}).data,
		        ChannelSerializer(
					Channel.published.filter(query),
					many=True,
					context={'request': request}).data,
		        GroupSerializer(
					Group.published.filter(query),
					many=True,
					context={'request': request}).data,
		        InstagramSerializer(
					Instagram.published.filter(query),
					many=True,
					context={'request': request}).data
			)
		else:
		    search_result = None

		return Response(search_result)


class CategoryListAPIView(ListAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	permission_classes = [AllowAny]
