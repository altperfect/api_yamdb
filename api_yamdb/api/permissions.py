from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка пользователя на наличие прав администратора."""
    message = "Пользователь не администратор."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка пользователя на наличие прав администратора
    для создания и редактирования записей.
    Если прав админа нет, то доступен только просмотр.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_admin):
            return True
        return False


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
