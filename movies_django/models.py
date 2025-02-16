from django.db import models
from django.contrib.auth import get_user_model
from config.models import *

# Create your models here.
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.user.username
    
