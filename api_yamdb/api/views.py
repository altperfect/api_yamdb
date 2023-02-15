from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import IsAdminModeratorAuthor
# from application.models import Title
from comments.serializers import CommentSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Создание и обработка произведений.
    Права доступа: Админ создёт и редактирует, остальные read only.
    """
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    ).select_related(
        "category"
    ).prefetch_related(
        "genre"
    ).all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Создание и обработка комментариев.
    Права доступа: Админ, Модератор, Автор.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        return super().get_queryset.filter(id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
