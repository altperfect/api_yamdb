from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'created')
