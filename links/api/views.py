from itertools import chain
from urllib.parse import unquote

from django.db.models import Q
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from taggit.models import Tag

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
	FilterByTypeMixIn,
	FilterByApplicationMixIn,
	PaginateMixIn,
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


class WebsiteListAPIView(FilterByTypeMixIn, ListAPIView):
	serializer_class = WebsiteSerializer
	queryset = Website.published.all()
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


class ChannelListAPIView(FilterByApplicationMixIn, ListAPIView):
	serializer_class = ChannelSerializer
	queryset = Channel.published.all()
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


class GroupListAPIView(FilterByApplicationMixIn, ListAPIView):
	serializer_class = GroupSerializer
	queryset = Group.published.all()
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


class CategoryListAPIView(ListAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	permission_classes = [AllowAny]


class CategorizedItemsAPIListView(PaginateMixIn, GenericAPIView):
	"""
	Get categorized items by category id
	"""
	permission_classes = [AllowAny]
	pagination_class = LinkPageNumberPagination

	def get_queryset(self):
		category_id = self.kwargs.get('category_id')
		websites = Website.published.filter(category_id=category_id)
		channels = Channel.published.filter(category_id=category_id)
		groups = Group.published.filter(category_id=category_id)
		instagrams = Instagram.published.filter(category_id=category_id)

		serialized_websites = WebsiteSerializer(websites, many=True,
			context={'request': self.request})
		serialized_channels = ChannelSerializer(channels, many=True,
			context={'request': self.request})
		serialized_groups = GroupSerializer(groups, many=True,
			context={'request': self.request})
		serialized_instagrams = InstagramSerializer(instagrams, many=True,
			context={'request': self.request})

		chained_links = chain(serialized_websites.data,
			serialized_channels.data,
			serialized_groups.data,
			serialized_instagrams.data
		)
		return list(chained_links)


class TaggedItemsAPIListView(PaginateMixIn, GenericAPIView):
	"""
	Get tagged items by tag slug
	"""
	permission_classes = [AllowAny]
	pagination_class = LinkPageNumberPagination

	def get_queryset(self):
		tag_slug = self.kwargs.get('tag_slug')
		tag_slug = unquote(tag_slug)
		tag = get_object_or_404(Tag, slug=tag_slug)

		websites = Website.published.filter(tags__in=[tag])
		channels = Channel.published.filter(tags__in=[tag])
		groups = Group.published.filter(tags__in=[tag])
		instagrams = Instagram.published.filter(tags__in=[tag])

		serialized_websites = WebsiteSerializer(websites, many=True,
			context={'request': self.request})
		serialized_channels = ChannelSerializer(channels, many=True,
			context={'request': self.request})
		serialized_groups = GroupSerializer(groups, many=True,
			context={'request': self.request})
		serialized_instagrams = InstagramSerializer(instagrams, many=True,
			context={'request': self.request})

		chained_links = chain(serialized_websites.data,
			serialized_channels.data,
			serialized_groups.data,
			serialized_instagrams.data
		)
		return list(chained_links)


class LinkSearchAPIView(PaginateMixIn, GenericAPIView):
	"""
	Search items by given query named `q`
	"""
	permission_classes = [AllowAny]
	pagination_class = LinkPageNumberPagination

	def get_queryset(self):
		q = self.request.GET.get('q')
		if q:
		    query = (Q(title__icontains=q) | Q(description__icontains=q))

		    # search the query in published links
		    search_result = chain(
		        WebsiteSerializer(
					Website.published.filter(query),
					many=True,
					context={'request': self.request}).data,
		        ChannelSerializer(
					Channel.published.filter(query),
					many=True,
					context={'request': self.request}).data,
		        GroupSerializer(
					Group.published.filter(query),
					many=True,
					context={'request': self.request}).data,
		        InstagramSerializer(
					Instagram.published.filter(query),
					many=True,
					context={'request': self.request}).data
			)
		else:
		    return None
		return list(search_result)
