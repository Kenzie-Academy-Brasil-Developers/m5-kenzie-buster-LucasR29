from rest_framework.views import Request, View
from rest_framework import permissions
from users.models import User

# SAFE_METHODS = (GET, OPTIONS, HEAD)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User) -> bool:
        if user == request.user:
            return True
        elif request.user.is_superuser:
            return True
