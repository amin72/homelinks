from PIL import Image
from django.db.models import Q
from django.utils.text import slugify
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
	WebsiteListSerializer,
	WebsiteDetailSerializer,
	WebsiteCreateSerializer,
	WebsiteUpdateSerializer,

	ChannelListSerializer,
	ChannelDetailSerializer,
	ChannelCreateSerializer,
	ChannelUpdateSerializer,

	GroupListSerializer,
	GroupDetailSerializer,
	GroupCreateSerializer,
	GroupUpdateSerializer,

	InstagramListSerializer,
	InstagramDetailSerializer,
	InstagramCreateSerializer,
	InstagramUpdateSerializer,
)

from links.mixins import (
	CreateAPIMixIn,
	RetrieveUpdateAPIMixIn,
	DeleteAPIMixIn,
)

from links import utils
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


@api_view()


def index(request):
	websites = Website.published.all()[:6]
	channels = Channel.published.all()[:6]
	groups = Group.published.all()[:6]
	instagrams = Instagram.published.all()[:6]

	serialized_websites = WebsiteListSerializer(websites, many=True,
		context={'request': request})
	serialized_channels = ChannelListSerializer(channels, many=True,
		context={'request': request})
	serialized_groups = GroupListSerializer(groups, many=True,
		context={'request': request})
	serialized_instagrams = InstagramListSerializer(instagrams, many=True,
		context={'request': request})

	result = {
		'websites': serialized_websites.data,
		'channels': serialized_channels.data,
		'groups': serialized_groups.data,
		'instagram': serialized_instagrams.data,
	}
	return Response(result)
class WebsiteListAPIView(ListAPIView):
    serializer_class = WebsiteListSerializer
    queryset = Website.published.all()
    pagination_class = PostPageNumberPagination


class IranianWebsiteListAPIView(ListAPIView):
    serializer_class = WebsiteListSerializer
    queryset = Website.published.filter(type='iranian')
    pagination_class = PostPageNumberPagination


class ForeignWebsiteListAPIView(ListAPIView):
    serializer_class = WebsiteListSerializer
    queryset = Website.published.filter(type='foreign')
    pagination_class = PostPageNumberPagination


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
    serializer_class = ChannelListSerializer
    queryset = Channel.published.all()
    pagination_class = PostPageNumberPagination


class TelegramChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer
    queryset = Channel.published.filter(application='telegram')
    pagination_class = PostPageNumberPagination


class SoroushChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer
    queryset = Channel.published.filter(application='soroush')
    pagination_class = PostPageNumberPagination


class GapChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer
    queryset = Channel.published.filter(application='gap')
    pagination_class = PostPageNumberPagination


class IGapChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer
    queryset = Channel.published.filter(application='igap')
    pagination_class = PostPageNumberPagination


class EitaaChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer
    queryset = Channel.published.filter(application='eitaa')
    pagination_class = PostPageNumberPagination


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
    serializer_class = GroupListSerializer
    queryset = Group.published.all()
    pagination_class = PostPageNumberPagination


class WhatsappGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='whatsapp')
    pagination_class = PostPageNumberPagination


class TelegramGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='telegram')
    pagination_class = PostPageNumberPagination


class SoroushGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='soroush')
    pagination_class = PostPageNumberPagination


class GapGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='gap')
    pagination_class = PostPageNumberPagination


class IGapGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='igap')
    pagination_class = PostPageNumberPagination


class EitaaGroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer
    queryset = Group.published.filter(application='eitaa')
    pagination_class = PostPageNumberPagination


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
    serializer_class = InstagramListSerializer
    queryset = Instagram.published.all()
    pagination_class = PostPageNumberPagination


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
