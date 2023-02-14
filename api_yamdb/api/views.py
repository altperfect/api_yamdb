from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from api.permissions import IsAdmin
from application.serializers import(
    TitleSerializer,
    CategorySerializer,
    GenreSerializer)
from application.models import Title, Category, Genre

class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
