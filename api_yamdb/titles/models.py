from django.db import models
from .validator import validate_year

class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256, verbose_name='название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='ссылка')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='название жанра'
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='ссылка')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.IntegerField(verbose_name='год', validators=[validate_year])
    description = models.TextField(
        max_length=256,
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

    class Meta:
        ordering = ('-year',)
        verbose_name = 'название'
        verbose_name_plural = 'названия'

    def __str__(self):
        return self.name
