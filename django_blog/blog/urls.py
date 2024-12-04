from django.urls import path
from django.contrib.auth import views as auth_views  # Importing built-in views
from . import views

urlpatterns = [
    # Login view
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # Logout view (it will automatically redirect to home page or can be specified)
    path('logout/', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    # Register view (uses your custom registration view)
    path('register/', views.register, name='register'),
    # Profile view (uses your custom profile view)
    path('profile/', views.profile, name='profile'),
    # Home view 
    path('home/', views.home, name='home'),
    # List posts view
    path('posts/', views.ListView, name='posts'),
    # Detail post view
    path('posts/<int:pk>/', views.DetailView, name='post-detail'),
    # Create post view
    path('post/new/ ', views.CreatView, name='post-create'),
    # Edit post view
    path('post/<int:pk>/update/', views.UpdateView, name='post-edit'),
    # Delete post view
    path('post/<int:pk>/delete/', views.DeleteView, name='post-delete'),
]

# Comment URL patterns 
urlpatterns += [
    # List comments view url
    path('post/<int:pk>/comments/', views.ListViewComment, name='comment-list'),
    # Detail comment view url
    path('post/<int:pk>/comments/new/', views.CommentCreateView, name='comment-create'),
    # Update comment view url
    path('post/<int:pk>/comment/<int:pk>/update/', views.CommentUpdateView, name='comment-update'),
    # Delete comment view url
    path('post/<int:pk>/comment/<int:pk>/delete/', views.CommentDeleteView, name='comment-delete'),
]