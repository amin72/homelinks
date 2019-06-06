from itertools import chain

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

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
)

from .serializers import (
	WebsiteSerializer,
	ChannelSerializer,
    GroupSerializer,
    InstagramSerializer,
	UserUpdateSerializer,
	UserCreateSerializer,
)

from dashboard.mixins import (
	ReplaceChildWithParentMixIn,
)

from links.mixins import PaginateMixIn

#from dashboard import utils
from links.api.pagination import (
	LinkLimitOffsetPagination,
	LinkPageNumberPagination,
)
from dashboard import utils


User = get_user_model()


class LinkListAPIView(PaginateMixIn, GenericAPIView):
	"""
	List and paginate all user's links
	"""
	pagination_class = LinkPageNumberPagination

	def get_queryset(self):
		user = self.request.user
		sorted_links = utils.get_sorted_users_links(user)
		# if links have child, sent their child instead of them.
		links_and_children = utils.replace_child_with_parent(sorted_links)

		users_links = []
		for link in links_and_children:
			if link.model_name == 'website':
				users_links.append(WebsiteSerializer(link,
				context={'request': self.request}).data)
			elif link.model_name == 'channel':
				users_links.append(ChannelSerializer(link,
				context={'request': self.request}).data)
			elif link.model_name == 'group':
				users_links.append(GroupSerializer(link,
				context={'request': self.request}).data)
			elif link.model_name == 'instagram':
				users_links.append(InstagramSerializer(link,
				context={'request': self.request}).data)
		return users_links


class UserWebsiteListAPIView(ReplaceChildWithParentMixIn):
	serializer_class = WebsiteSerializer
	pagination_class = LinkPageNumberPagination
	model = Website


class UserChannelListAPIView(ReplaceChildWithParentMixIn):
	serializer_class = ChannelSerializer
	pagination_class = LinkPageNumberPagination
	model = Channel


class UserGroupListAPIView(ReplaceChildWithParentMixIn):
	serializer_class = GroupSerializer
	pagination_class = LinkPageNumberPagination
	model = Group


class UserInstagramListAPIView(ReplaceChildWithParentMixIn):
	serializer_class = InstagramSerializer
	pagination_class = LinkPageNumberPagination
	model = Instagram


class UserUpdateAPIView(APIView):
	serializer_class = UserUpdateSerializer
	model = User

	def get(self, request, format=None):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data)

	def put(self, request, format=None):
		serializer = self.serializer_class(request.user, request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=200)
		return Response(serializer.errors, status=401)


class UserRegisterAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	permission_classes = [AllowAny]
	model = User
