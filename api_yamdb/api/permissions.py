from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверка пользователя на права администратора.
    Иначе ReadOnly.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )
