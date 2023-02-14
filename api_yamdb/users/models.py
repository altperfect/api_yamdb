from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_confirmation_code


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
