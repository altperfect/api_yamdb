from django_filters import rest_framework as django_filters

from reviews.models import Title


class TitleGenreFilter(django_filters.FilterSet):
    """
    Фильтр для TitleViewSet.
    Реализует возможность фильтрации по полю 'genre'
    с использованием параметра 'slug' жанра.
    """

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    genre = django_filters.CharFilter(
        field_name="genre__slug",
        lookup_expr="icontains"
    )
    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="icontains"
    )
    year = django_filters.NumberFilter(
        field_name="year",
        lookup_expr="icontains"
    )

    class Meta:
        model = Title
        fields = ("name", "genre", "category", "year")
