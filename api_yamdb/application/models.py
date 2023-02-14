from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='ссылка')

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

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=200, verbose_name='название')
    year = models.IntegerField(verbose_name='год')
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

    def __str__(self):
        return self.name
