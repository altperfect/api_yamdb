from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from comments.serializers import CommentSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from titles.models import Title


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ...

    def get_queryset(self):
        return super().get_queryset.filter(id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ...

    def get_queryset(self):
        return super().get_queryset.filter(id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
