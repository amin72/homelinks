from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
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
)

from links.mixins import (
	CreateAPIMixIn,
	RetrieveUpdateAPIMixIn,
	DeleteAPIMixIn,
)

from links import utils
from .pagination import LinkLimitOffsetPagination, LinkPageNumberPagination


@api_view()
def index(request):
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


class IranianWebsiteListAPIView(ListAPIView):
    serializer_class = WebsiteSerializer
    queryset = Website.published.filter(type='iranian')
    pagination_class = LinkPageNumberPagination


class ForeignWebsiteListAPIView(ListAPIView):
    serializer_class = WebsiteSerializer
    queryset = Website.published.filter(type='foreign')
    pagination_class = LinkPageNumberPagination


class WebsiteDetailAPIView(RetrieveAPIView):
	serializer_class = WebsiteDetailSerializer
	queryset = Website.published.all()
	lookup_field = 'slug'


class WebsiteCreateAPIView(CreateAPIMixIn):
	serializer_class = WebsiteCreateSerializer


class WebsiteUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = WebsiteUpdateSerializer
	queryset = Website.published.all()
	lookup_field = 'slug'
	model = Website


class WebsiteDeleteAPIView(DeleteAPIMixIn):
	queryset = Website.published.all()
	lookup_field = 'slug'
#----------------------------------------------------------


class ChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.all()
    pagination_class = LinkPageNumberPagination


class TelegramChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.filter(application='telegram')
    pagination_class = LinkPageNumberPagination


class SoroushChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.filter(application='soroush')
    pagination_class = LinkPageNumberPagination


class GapChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.filter(application='gap')
    pagination_class = LinkPageNumberPagination


class IGapChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.filter(application='igap')
    pagination_class = LinkPageNumberPagination


class EitaaChannelListAPIView(ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.published.filter(application='eitaa')
    pagination_class = LinkPageNumberPagination


class ChannelDetailAPIView(RetrieveAPIView):
	serializer_class = ChannelDetailSerializer
	queryset = Channel.published.all()
	lookup_field = 'slug'


class ChannelCreateAPIView(CreateAPIMixIn):
	serializer_class = ChannelCreateSerializer


class ChannelUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = ChannelUpdateSerializer
	queryset = Channel.published.all()
	lookup_field = 'slug'
	model = Channel


class ChannelDeleteAPIView(DestroyAPIView):
	queryset = Channel.published.all()
	lookup_field = 'slug'


class ChannelDeleteAPIView(DeleteAPIMixIn):
	queryset = Channel.published.all()
	lookup_field = 'slug'
# ---------------------------------------------------------


class GroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.all()
    pagination_class = LinkPageNumberPagination


class WhatsappGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='whatsapp')
    pagination_class = LinkPageNumberPagination


class TelegramGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='telegram')
    pagination_class = LinkPageNumberPagination


class SoroushGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='soroush')
    pagination_class = LinkPageNumberPagination


class GapGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='gap')
    pagination_class = LinkPageNumberPagination


class IGapGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='igap')
    pagination_class = LinkPageNumberPagination


class EitaaGroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.published.filter(application='eitaa')
    pagination_class = LinkPageNumberPagination


class GroupDetailAPIView(RetrieveAPIView):
	serializer_class = GroupDetailSerializer
	queryset = Group.published.all()
	lookup_field = 'slug'


class GroupCreateAPIView(CreateAPIMixIn):
	serializer_class = GroupCreateSerializer


class GroupUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = GroupUpdateSerializer
	queryset = Group.published.all()
	lookup_field = 'slug'
	model = Group


class GroupDeleteAPIView(DestroyAPIView):
	queryset = Group.published.all()
	lookup_field = 'slug'


class GroupDeleteAPIView(DeleteAPIMixIn):
	queryset = Group.published.all()
	lookup_field = 'slug'
# --------------------------------------------------------


class InstagramListAPIView(ListAPIView):
    serializer_class = InstagramSerializer
    queryset = Instagram.published.all()
    pagination_class = LinkPageNumberPagination


class InstagramDetailAPIView(RetrieveAPIView):
	serializer_class = InstagramDetailSerializer
	queryset = Instagram.published.all()
	lookup_field = 'slug'


class InstagramCreateAPIView(CreateAPIMixIn):
	serializer_class = InstagramCreateSerializer


class InstagramUpdateAPIView(RetrieveUpdateAPIMixIn):
	serializer_class = InstagramUpdateSerializer
	queryset = Instagram.published.all()
	lookup_field = 'slug'
	model = Instagram


class InstagramDeleteAPIView(DeleteAPIMixIn):
	queryset = Instagram.published.all()
	lookup_field = 'slug'
	model = Instagram
# ---------------------------------------------------------


class ReportLinkAPIView(CreateAPIView):
	serializer_class = LinkReportSerializer

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
            content_type=content_type,
            object_id=obj.id,
            url=obj.url,
        )

		return serializer
