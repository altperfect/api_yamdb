from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка пользователя на права администрасора."""
    message = 'Пользователь не является администратором'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or request.user.is_superuser
