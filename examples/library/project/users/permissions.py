from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class IsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj
