from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import (
    forbidden_username_validator,
    username_validator
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True
    )

    class Meta:
        fields = ("id", "review", "author", "text", "pub_date")
        model = Comment
        read_only_fields = ("id", "pub_date")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )

    def validate_score(self, value):
        """Проверка оценки на соответствие 10-бальной шкале."""
        if 0 > value > 10:
            raise serializers.ValidationError(
                "Оценка должна быть по 10-бальной шкале!"
            )
        return value

    def validate(self, data):
        """Проверка отзыва. Создать можно только один отзыв."""
        request = self.context.get("request")
        if request and request.method == "POST":
            title_id = self.context["view"].kwargs.get("title_id")
            if Review.objects.filter(
                author=request.user,
                title=title_id
            ).exists():
                raise serializers.ValidationError(
                    "Можно оставить только один отзыв."
                )
        return data

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = ("id", "pub_date")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"

    def validate_year(self, value):
        """
        Проверка года выпуска.
        Год должен быть не позже текущего года.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Проверьте дату создания произведения."
            )
        return value

    def validate_title(self, validated_data):
        """Проверка произведения на дубликат."""
        request = self.context.get("request")
        if request and request.method == "POST":
            if Title.objects.filter(
                name=validated_data.get("name"),
                category=validated_data.get("category")
            ).exists():
                raise serializers.ValidationError(
                    "Произведение уже существует."
                )
        return validated_data


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели произведений,
    используется в ReadOnly сценариях.
    """

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = "__all__"


class SignUpSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации.
    Использовать служебное имя "me" запрещено.
    """

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=(
            forbidden_username_validator,
            username_validator
        )
    )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                "Нельзя использовать логин 'me'."
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Пользователя."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "bio", "role")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для создания JWT-токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
