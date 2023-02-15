from rest_framework import viewsets, permissions
from api.permissions import IsAdminOrReadOnly
from titles.serializers import(
    TitleSerializer,
    CategorySerializer,
    GenreSerializer)
from titles.models import Title, Category, Genre

class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка произведений доступно без токена.
    Админ создает и редактирует.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Получение списка категорий доступно без токена.
    Админ создает и редактирует.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """
    Получение списка жанров доступно без токена.
    Админ создает и редактирует.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
