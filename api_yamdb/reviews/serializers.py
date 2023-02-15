from reviews.models import Review, Title
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate_score(self, value):
        """Проверка оценки на соответствие 10-бальной шкале."""
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть по 10-бальной шкале!'
            )
        return value

    def validate_review(self, data):
        """Проверка отзыва. Создать можно только один отзыв."""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (
            request.method == 'POST' and Review.objects.filter(
                title=title, author=author
            ).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'created')
