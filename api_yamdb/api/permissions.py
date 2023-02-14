from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка пользователя на наличие прав администратора."""
    message = "Пользователь не администратор."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAdminModeratorAuthor(permissions.BasePermission):
    """
    Проверка пользователя на наличие одного из типов прав:
    администратора, модератора или автора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )
