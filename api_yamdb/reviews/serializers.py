from rest_framework import serializers

from comments.models import Review


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
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть по 10-бальной шкале!'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'created')