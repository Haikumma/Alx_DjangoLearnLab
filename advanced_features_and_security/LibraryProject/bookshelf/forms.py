from django.contrib.auth.forms import UserCreationForm
from .models import Book


class ExampleForm(UserCreationForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']