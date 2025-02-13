from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size, poster_validator, trailer_validator
from django.db.models import Avg

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(default=0)
    poster = models.ImageField(
        upload_to='movies/posters/', 
        null=True, 
        blank=True,
        validators=[poster_validator, validate_file_size]
    )
    trailer = models.FileField(
        upload_to='movies/trailers/',
        null=True,
        blank=True,
        validators=[trailer_validator, validate_file_size]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    language = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    actors = models.TextField()
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating else 0
        self.save()

    def increment_views(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_rating()

    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_rating()

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"
