from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class CustomUser (AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    objects = CustomUserManager()
