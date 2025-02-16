from django.urls import path
from .views import movie_list, movie_detail

urlpatterns = [
    path('', movie_list, name='movie_list'),  # Barcha kinolar
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),  # Kino tafsilotlari
]
