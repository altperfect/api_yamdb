from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from application.models import Title
from comments.serializers import CommentSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from users.models import User
from users.serializers import UserSerializer
from api.permissions import IsAdmin
from application.serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer)
from application.models import Title, Category, Genre

from api.permissions import IsAdmin, IsAdminModeratorAuthor


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.annotate(
        review_raiting=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Создание и обработка отзывов.
    Права доступа: Админ, Модератор, Автор.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        return super().get_queryset.filter(id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    search_fields = ("username",)
    filter_backends = (SearchFilter,)
    http_method_names = ["get", "post", "delete", "patch"]

