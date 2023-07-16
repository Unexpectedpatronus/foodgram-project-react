from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Доступ имеют администраторы, авторы объектов.
    Для остальных - только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_staff or obj.author == request.user))
