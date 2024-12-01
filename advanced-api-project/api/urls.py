from django.urls import path
from .views import BookListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('books/', BookListView.as_view()),
    path('books/<int:pk>/', DetailView.as_view()),
    path('books/create/', CreateView.as_view()),
    path('books/update<int:pk>/', UpdateView.as_view()),
    path('books/delete/<int:pk>/', DeleteView.as_view())

]