from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsCollectionOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, action):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
