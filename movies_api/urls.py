from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from movies_api import views
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ReviewViewSet, GenreViewSet, PersonViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = [
    # API
    path('movies/', views.MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # REST framework auth URLs
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT token URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('register/', views.RegisterView.as_view(), name='register'),

    # Genre URLs
    path('genres/', views.GenreViewSet.as_view({'get': 'list', 'post': 'create'}), name='genre-list'),
    path('genres/<int:pk>/', views.GenreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='genre-detail'),

    path('persons/', views.PersonViewSet.as_view({'get': 'list', 'post': 'create'}), name='person-list'),
    path('persons/<int:pk>/', views.PersonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='person-detail'),

    path('countries/', views.CountryViewSet.as_view({'get': 'list', 'post': 'create'}), name='country-list'),
    path('countries/<int:pk>/', views.CountryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='country-detail'),

    path('', include(router.urls)),
]
