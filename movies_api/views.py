from django.shortcuts import render
from rest_framework import generics, filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Count, Avg
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from config.models import (
    Movie, Review, Genre, Person, Country, 
    MovieImage,
    Collection,  MovieList, MovieReport,
    MovieSeason, MovieEpisode, UserActivity
)
from movies_django.models import UserProfile
from movies_api.serializers import (
    MovieListSerializer, MovieDetailSerializer, ReviewSerializer, MovieSerializer,
    GenreSerializer, PersonSerializer, CountrySerializer,
    MovieCastSerializer, MovieImageSerializer, AwardSerializer,
    MovieAwardSerializer, SubtitleSerializer, CollectionSerializer,
    UserProfileSerializer, MovieListStatusSerializer,
    MovieReportSerializer, MovieSeasonSerializer,
    MovieEpisodeSerializer, UserActivitySerializer,
    NotificationSerializer, RegisterSerializer, UserSerializer
)
from movies_api.pagination import MovieListPagination, ReviewListPagination, CollectionListPagination
from movies_api.permissions import (
    IsAdminOrReadOnly, IsOwnerOrReadOnly, 
    IsCollectionOwnerOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from movies_api.throttling import AnonMovieRateThrottle, UserMovieRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from movies_api.filters import MovieFilter

User = get_user_model()

# Create your views here.

class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [UserMovieRateThrottle]
    pagination_class = MovieListPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'rating', 'created_at']

    @swagger_auto_schema(
        operation_description="Get list of movies",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title and description", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="Create a new movie (Admin only)")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        movie = serializer.save()
        users = User.objects.all()
        for user in users:
            if user.email:
                send_mail(
                    'Yangi film qo\'shildi!',
                    f'Yangi film: {movie.title}\nTavsif: {movie.description}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [UserMovieRateThrottle]

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie')
        user = request.user

        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=user)  
            
            
            movie = Movie.objects.get(id=movie_id)
            movie.update_rating() 
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            review = serializer.save() 
            
            
            movie = instance.movie
            movie.update_rating()  
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [UserMovieRateThrottle]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FeaturedMoviesView(generics.ListAPIView):
    queryset = Movie.objects.filter(is_featured=True)
    serializer_class = MovieListSerializer

class TopRatedMoviesView(generics.ListAPIView):
    queryset = Movie.objects.order_by('-rating')[:10]
    serializer_class = MovieListSerializer

class MostViewedMoviesView(generics.ListAPIView):
    queryset = Movie.objects.order_by('-views_count')[:10]
    serializer_class = MovieListSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated, IsCollectionOwnerOrReadOnly]
    pagination_class = CollectionListPagination

    def get_queryset(self):
        return Collection.objects.filter(
            created_by=self.request.user
        ).prefetch_related('movies')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_movie(self, request, pk=None):
        collection = self.get_object()
        movie_id = request.data.get('movie_id')
        
        try:
            movie = Movie.objects.get(id=movie_id)
            collection.movies.add(movie)
            return Response({'status': 'movie added'})
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class MovieReportViewSet(viewsets.ModelViewSet):
    serializer_class = MovieReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return MovieReport.objects.all()
        return MovieReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MovieSeasonViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSeasonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_pk')
        return MovieSeason.objects.filter(movie_id=movie_id)

class MovieEpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = MovieEpisodeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        season_id = self.kwargs.get('season_pk')
        return MovieEpisode.objects.filter(season_id=season_id)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)
    
