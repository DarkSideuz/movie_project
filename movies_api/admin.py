from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'has_poster', 'has_trailer', 'created_at')
    list_filter = ('release_date', 'rating')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'release_date'
    readonly_fields = ('created_at', 'updated_at')

    def has_poster(self, obj):
        return bool(obj.poster)
    has_poster.boolean = True
    has_poster.short_description = 'Poster'

    def has_trailer(self, obj):
        return bool(obj.trailer)
    has_trailer.boolean = True
    has_trailer.short_description = 'Treyler'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')
    ordering = ('-created_at',)
    raw_id_fields = ('movie', 'user')
