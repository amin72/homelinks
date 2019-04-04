from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
)


class LinkLimitOffsetPagination(LimitOffsetPagination):
	max_limit = 10
	default_limit = 20


class LinkPageNumberPagination(PageNumberPagination):
	page_size = 20
