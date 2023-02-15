from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления пользователями.
    Доступ на создание: только у администратора.
    Доступ на редактирование: у зарегистрированных пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    search_fields = ("username",)
    filter_backends = (SearchFilter,)
    http_method_names = ["get", "post", "delete", "patch"]

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
