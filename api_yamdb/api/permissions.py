from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка пользователя на наличие прав администратора."""
    message = "Пользователь не администратор."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or request.user.is_superuser
