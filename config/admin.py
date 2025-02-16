from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie, Review, Genre, Person, Country
from unfold.admin import ModelAdmin


@admin.register(Movie)
class CustomAdminClass(ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'is_featured')
    search_fields = ('title', 'description')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'birth_date')
    list_filter = ('role',)
    search_fields = ('name', 'bio')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')

admin.site.register(Genre)
admin.site.register(Country)