from rest_framework import serializers
from django.utils import timezone
from .models import Title, Category, Genre

class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'
    
    def validate_year(self, value):
        current_year = timezone.now().year
        if not value <= current_year:
            raise serializers.ValidationError(
                'Проверьте дату создания произведения'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
