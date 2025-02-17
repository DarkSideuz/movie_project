from django.shortcuts import render, get_object_or_404
from config.models import Movie, Review

# Create your views here.

def movie_list(request):
    movies = Movie.objects.all() 
    return render(request, 'index.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.review.all()  


