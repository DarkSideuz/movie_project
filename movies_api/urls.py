from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
