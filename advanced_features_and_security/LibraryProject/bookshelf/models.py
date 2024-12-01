from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    class Meta:
        permissions = [
            ('can_view_book', 'Can view book'),
            ('can_create_book', 'Can create book'),
            ('can_edit_book', 'Can edit book'),
            ('can_delete_book', 'Can delete book')
            ]
    
 class CustomUserManager(BaseUserManager):
     def create_user(self, email, password=None, **extra_fields):
         if not email:
            raise ValueError('Email is required')
         if not password:
             raise ValueError('Password is required')
         email = self.normalize_email(email)
         user = self.model(email=email, **extra_fields)
         user.set_password(password)
         user.save()
         return user
     def create_superuser(self, email, password=None, **extra_fields):
         extra_fields.setdefault('is_staff', True)
         extra_fields.setdefault('is_superuser', True)
         return self.create_user(email, password, **extra_fields)
 class CustomUser(AbstractUser):
     email = models.EmailField(unique=True)
     date_of_birth = models.DateField(max_length=200)
     profile_photo = models.ImageField()
     is_staff = models.BooleanField(default=False)
     is_active = models.BooleanField(default=True)
     is_superuser = models.BooleanField(default=False)

     objects = CustomUserManager()

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['first_name', 'last_name']

