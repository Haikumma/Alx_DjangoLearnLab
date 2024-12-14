from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

# custom user manager to handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and saves a User with the given username, email and
        password. Other fields can be set with keyword arguments.
        
        :param username: The username of the user
        :param email: The email address of the user
        :param password: The password of the user
        :param extra_fields: Additional fields to set on the user
        :raises ValueError: If the username or email is not set
        :return: The created User"""

        if not username:
            raise ValueError("The username field must be set")
        
        if not email:
            raise ValueError("The email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        """Creates and saves a User with the given username and password.

        :param username: The username of the user
        :param password: The password of the user
        :param extra_fields: Additional fields to set on the user
        :raises ValueError: If the username is not set
        :return: The created User

        This method sets ``is_staff`` and ``is_superuser`` to True before calling
        the parent class's ``create_user`` method. This means that the user will
        be able to log in to the Django admin site and have all the permissions
        granted to the user type."""
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)

# custom user model to extend user fields
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=1000, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  ['first_name', 'last_name']

    objects = CustomUserManager()