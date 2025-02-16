from django_filters import rest_framework as filters
from .models import Movie, Review, Collection

class MovieFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    min_year = filters.NumberFilter(field_name="release_date", lookup_expr='year__gte')
    max_year = filters.NumberFilter(field_name="release_date", lookup_expr='year__lte')
    genre = filters.CharFilter(field_name='genres__name', lookup_expr='iexact')
    director = filters.CharFilter(field_name='directors__name', lookup_expr='icontains')
    actor = filters.CharFilter(field_name='actors__name', lookup_expr='icontains')
    country = filters.CharFilter(field_name='countries__name', lookup_expr='iexact')
    language = filters.ChoiceFilter(choices=Movie.LANGUAGE_CHOICES)
    age_rating = filters.ChoiceFilter(choices=Movie.AGE_RATINGS)
    is_featured = filters.BooleanFilter(field_name='is_featured')
    
    class Meta:
        model = Movie
        fields = [
            'min_rating', 'max_rating', 'min_year', 'max_year',
            'genre', 'director', 'actor', 'country', 'language',
            'age_rating', 'is_featured', 'title', 'release_date'
        ]

class ReviewFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    movie = filters.NumberFilter(field_name="movie__id")
    user = filters.NumberFilter(field_name="user__id")
    
    class Meta:
        model = Review
        fields = ['min_rating', 'max_rating', 'movie', 'user']

class CollectionFilter(filters.FilterSet):
    created_by = filters.NumberFilter(field_name="created_by__id")
    is_public = filters.BooleanFilter()
    
    class Meta:
        model = Collection
        fields = ['created_by', 'is_public']
