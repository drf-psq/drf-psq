from rest_framework import permissions


class IsRegisteredInLibrary(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):  # 'obj' is of type Library
        return request.user.registered_library == obj
