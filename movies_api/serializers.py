from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from config.models import (
    Movie, Review, Genre, Person, Country, MovieCast, 
    Watchlist, MovieImage, Award, MovieAward, Subtitle,
    Collection, MovieList, MovieReport,
    MovieSeason, MovieEpisode, UserActivity, Notification
)
from movies_django.models import UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'birth_date', 'favorite_genres', 'following']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return user

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class MovieCastSerializer(serializers.ModelSerializer):
    actor = PersonSerializer(read_only=True)
    
    class Meta:
        model = MovieCast
        fields = ['id', 'actor', 'character_name', 'is_main_character']

class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ['id', 'image', 'is_banner', 'created_at']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'comment', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'release_date',
            'rating', 'poster', 'views_count'
        ]

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    directors = PersonSerializer(many=True, read_only=True)
    cast = MovieCastSerializer(source='moviecast_set', many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    images = MovieImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'description', 
            'release_date', 'duration', 'rating', 'poster', 
            'trailer', 'genres', 'directors', 'cast', 
            'countries', 'language', 'age_rating', 'budget',
            'box_office', 'is_featured', 'views_count',
            'images', 'reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['rating', 'views_count']

class MovieSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSeason
        fields = ['id', 'season_number', 'title', 'description', 'release_date']

class MovieEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieEpisode
        fields = ['id', 'episode_number', 'title', 'description', 'duration', 'video_file', 'air_date']

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'name', 'organization', 'description']

class MovieAwardSerializer(serializers.ModelSerializer):
    award = AwardSerializer(read_only=True)
    
    class Meta:
        model = MovieAward
        fields = ['id', 'award', 'year', 'category', 'winner']

class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['id', 'language', 'subtitle_file']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'movies', 'created_by', 'is_public', 'created_at']
        read_only_fields = ['created_by']

class MovieListStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieList
        fields = ['id', 'movie', 'list_type', 'added_at']
        read_only_fields = ['user']

class MovieReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReport
        fields = ['id', 'movie', 'report_type', 'description', 'is_resolved', 'created_at']
        read_only_fields = ['user', 'is_resolved', 'resolved_at']

class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'activity_type', 'movie', 'review', 'target_user', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']
