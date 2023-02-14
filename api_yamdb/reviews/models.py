from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from application.models import Title
from users.models import User


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
    pub_date = models.DateField(
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
