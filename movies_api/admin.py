from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'created_at')
    list_filter = ('release_date', 'rating')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'release_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')
    ordering = ('-created_at',)
    raw_id_fields = ('movie', 'user')
