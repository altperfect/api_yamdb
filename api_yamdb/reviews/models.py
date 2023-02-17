from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.utils import generate_confirmation_code


class User(AbstractUser):
    """Модель создания пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'

    ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
        (SUPERUSER, 'superuser'),
    ]

    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE,
        default='user'
    )
    bio = models.TextField(
        'О себе',
        blank=True,
        null=True,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=32,
        unique=True,
        default=generate_confirmation_code,
        verbose_name="Код подтверждения"
    )

    @property
    def is_admin(self):
        """Проверяем наличие прав суперюзера."""
        return self.role == self.is_superuser

    @property
    def is_admin(self):
        """Проверяем наличие прав администратора."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Проверяем наличие прав модератора."""
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        """Проверяем наличие стандартных прав."""
        return self.role == self.USER

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = (
            models.UniqueConstraint(
                fields=("username", "email"),
                name="unique_username_and_email"
            ),
            models.CheckConstraint(
                check=~models.Q(username="me"),
                name="me_username_forbidden"
            ),
        )

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='ссылка')

    class Meta():
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название жанра'
    )
    slug = models.SlugField(unique=True, verbose_name='ссылка')

    class Meta():
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=200,
        verbose_name='название'
    )
    year = models.IntegerField(
        verbose_name='год'
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categories',
        verbose_name='категория'
    )

    class Meta():
        ordering = ('-year',)
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для создания отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        default=0,
        blank=False,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validate_error': 'Оценка должна быть от 1 до 10.'
        },
        verbose_name='Оценка'
    )
    text = models.TextField(
        max_length=1200,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:settings.REVIEW_CUT]


class Comment(models.Model):
    """Модель для создания комментариев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        max_length=400,
        verbose_name='Комментарий',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text[:settings.COMMENT_CUT]
