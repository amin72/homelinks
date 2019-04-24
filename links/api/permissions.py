from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPremiumUser(BasePermission):
    message = _('Only premium users are allowed to do this operation')

    def has_permission(self, request, view):
        return request.user.is_premium


class IsOwner(BasePermission):
    message = _('You are not allowed to update/delete this link')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
