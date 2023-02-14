from rest_framework import serializers

from users.models import User
from users.validators import (
    me_username_forbidden_validator,
    username_validator
)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=(
            me_username_forbidden_validator,
            username_validator
        )
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Пользователя."""

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "bio", "role",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для создания JWT-токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
