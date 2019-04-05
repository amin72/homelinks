from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView

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
)

from .serializers import (
	WebsiteSerializer,
	ChannelSerializer,
    GroupSerializer,
    InstagramSerializer,
)

from dashboard.mixins import (
	ReplaceChildWithParentMixIn,
)

#from dashboard import utils
from links.api.pagination import (
	LinkLimitOffsetPagination,
	LinkPageNumberPagination,
)
from dashboard import utils


class LinkListAPIView(APIView):
	def get(self, request, format=None):
		user = self.request.user
		sorted_links = utils.get_sorted_users_links(user)
		# if links have child, sent their child instead of them.
		links_and_children = utils.replace_child_with_parent(sorted_links)

		serialized_links = []
		for link in links_and_children:
			if link.model_name == 'website':
				serialized_link = WebsiteSerializer(link,
					context={'request': request})
			elif link.model_name == 'channel':
				serialized_link = ChannelSerializer(link,
					context={'request': request})
			elif link.model_name == 'group':
				serialized_link = GroupSerializer(link,
					context={'request': request})
			elif link.model_name == 'instagram':
				serialized_link = InstagramSerializer(link,
					context={'request': request})

			serialized_links.append(serialized_link.data)

		# return latest 10 links to dashboard-index
		result = {
			'links': serialized_links[:10],
		}
		return Response(result)


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