from django_filters import rest_framework as filters
from .models import Movie

class MovieFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    genre = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter(field_name="release_date", lookup_expr='year')
    
    class Meta:
        model = Movie
        fields = ['min_rating', 'max_rating', 'genre', 'year']
