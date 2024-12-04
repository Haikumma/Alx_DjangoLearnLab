from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Custom User model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Store images in 'profile_pics/' folder
    bio = models.TextField(blank=True)

# Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    # Add the ManyToMany relationship with the Tag model
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return self.title

# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Tag model for tagging posts
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
