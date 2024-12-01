from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from . models import Book
from .models import Library
 
# Create your views here
def list_books(request):
    books = Book.objects.all()
    context = {
        'books' : books
    }
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library

    def specific_library(self, request, library_name):
        library = Library.objects.filter(name=library_name)
        context = {
            'library' : library
        }
        return render(request, 'relationship_app/library_detail.html', context)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'   
    Seccess_url = reverse_lazy('login') 

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


def is_admin(user):
    return user.UserProfile.filter(role='Admin').exists() 

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

def is_librarian(user):
    return user.UserProfile.filter(role='Librarian').exists()

@login_required(login_url='login')
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

def is_member(user):
    return user.UserProfile.filter(role='Member').exists()

@login_required(login_url='login')
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
from django.contrib.auth.decorators import permission_required
@permission_required('relationship_app.can_add_book')
def add_book(request):
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def change_book(request):
    return render(request, 'relationship_app/change_book.html')

@permission_required('relationship_app.can_delete_book')
def delete_book(request):
    return render(request, 'relationship_app/delete_book.html')