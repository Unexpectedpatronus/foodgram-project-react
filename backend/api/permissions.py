from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ имеет администратор или superuser, для остальных -
    только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ для автора, авторизованного пользователя.
    Для остальных - только чтение."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and obj.author == request.user)
