from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # MEDIA 
    avatar = models.ImageField(
        upload_to="profiles/avatars/", default="profiles/default-avatar.png", blank=True
    )
    cover_photo = models.ImageField(upload_to="profiles/covers/", default="profiles/default-cover.jpg", null=True, blank=True)

    # IDENTITY
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    
    # PERSONAL INFO
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)

    # PROFESSIONAL INFO
    education = models.CharField(max_length=255, blank=True)
    experience = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
 
    # META
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s profile"
