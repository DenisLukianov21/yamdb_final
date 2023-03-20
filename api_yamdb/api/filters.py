from django_filters import rest_framework as filter
from reviews.models import Title


class TitleFilter(filter.FilterSet):
    """Фильтрация поиска для произведений по разным критериями."""
    name = filter.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    category = filter.CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = filter.CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )
    year = filter.NumberFilter(
        field_name="year",
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
