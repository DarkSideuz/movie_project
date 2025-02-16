from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_file_size, poster_validator, trailer_validator
from django.db.models import Avg

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    ROLES = (
        ('ACTOR', 'Actor'),
        ('DIRECTOR', 'Director'),
        ('PRODUCER', 'Producer'),
        ('WRITER', 'Writer'),
    )
    
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='persons/', null=True, blank=True)
    role = models.CharField(max_length=100, choices=ROLES)
    
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class Movie(models.Model):
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('RU', 'Russian'),
        ('UZ', 'Uzbek'),
        ('KR', 'Korean'),
        ('TR', 'Turkish'),
        ('OTHER', 'Other'),
    )
    
    AGE_RATINGS = (
        ('G', 'General Audience'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parental Guidance for Children Under 13'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    )
    
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    rating = models.FloatField()
    poster = models.ImageField(upload_to='posters/', default='posters/default.jpg')
    trailer = models.FileField(
        upload_to='movies/trailers/',
        validators=[trailer_validator, validate_file_size]
    )
    genres = models.ManyToManyField(Genre, related_name='movies')
    directors = models.ManyToManyField(
        Person, 
        related_name='directed_movies',
        limit_choices_to={'role': 'DIRECTOR'}
    )
    actors = models.ManyToManyField(
        Person,
        through='MovieCast',
        related_name='acted_movies',
        limit_choices_to={'role': 'ACTOR'}
    )
    writers = models.ManyToManyField(
        Person,
        related_name='written_movies',
        limit_choices_to={'role': 'WRITER'}
    )
    producers = models.ManyToManyField(
        Person,
        related_name='produced_movies',
        limit_choices_to={'role': 'PRODUCER'}
    )
    countries = models.ManyToManyField(Country, related_name='movies')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    age_rating = models.CharField(max_length=10, default='PG')
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    box_office = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_rating(self):
        avg_rating = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.rating = round(avg_rating, 1) if avg_rating else 0
        self.save()

    def increment_views(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
            models.Index(fields=['rating']),
            models.Index(fields=['views_count']),
        ]

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'ACTOR'}
    )
    character_name = models.CharField(max_length=200)
    is_main_character = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.actor.name} as {self.character_name} in {self.movie.title}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user = self.user
        super().save(*args, **kwargs)
        if not self.pk:
            self.movie.update_rating()

    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_rating()

    def __str__(self):
        return f'Review for {self.movie.title} by {self.user.username}'
    
    class Meta:
        unique_together = ['movie', 'user']
        ordering = ['-created_at']

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'movie']

class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='movies/images/',
        validators=[poster_validator, validate_file_size]
    )
    is_banner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.movie.title}"

class Award(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class MovieAward(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='awards')
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    year = models.IntegerField()
    category = models.CharField(max_length=200)
    winner = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.movie.title} - {self.award.name} ({self.year})"

class Subtitle(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=50)
    subtitle_file = models.FileField(upload_to='movies/subtitles/')
    
    class Meta:
        unique_together = ['movie', 'language']

class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    movies = models.ManyToManyField(Movie, related_name='collections')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.user.username

class MovieList(models.Model):
    LIST_TYPES = (
        ('WATCH', 'Want to Watch'),
        ('WATCHING', 'Currently Watching'),
        ('WATCHED', 'Watched'),
        ('FAVORITE', 'Favorites'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    list_type = models.CharField(max_length=10, choices=LIST_TYPES)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'movie', 'list_type']

class MovieReport(models.Model):
    REPORT_TYPES = (
        ('BROKEN', 'Broken Video/Audio'),
        ('SUBTITLE', 'Subtitle Issue'),
        ('CONTENT', 'Inappropriate Content'),
        ('OTHER', 'Other Issue'),
    )
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Report for {self.movie.title} by {self.user.username}"

class MovieSeason(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    
    class Meta:
        unique_together = ['movie', 'season_number']
        ordering = ['season_number']

class MovieEpisode(models.Model):
    season = models.ForeignKey(MovieSeason, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    video_file = models.FileField(upload_to='movies/episodes/')
    air_date = models.DateField()
    
    class Meta:
        unique_together = ['season', 'episode_number']
        ordering = ['episode_number']

class UserActivity(models.Model):
    ACTIVITY_TYPES = (
        ('REVIEW', 'Added Review'),
        ('RATE', 'Rated Movie'),
        ('WATCH', 'Added to Watchlist'),
        ('LIKE', 'Liked Review'),
        ('FOLLOW', 'Followed User'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='target_activities')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
