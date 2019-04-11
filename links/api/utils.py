from rest_framework import serializers


# url details
WEBSITE_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:website-detail',
    lookup_field='slug',
)

CHANNEL_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:channel-detail',
    lookup_field='slug',
)

GROUP_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:group-detail',
    lookup_field='slug',
)

INSTAGRAM_DETAIL_URL = serializers.HyperlinkedIdentityField(
    view_name='links-apis:instagram-detail',
    lookup_field='slug',
)
