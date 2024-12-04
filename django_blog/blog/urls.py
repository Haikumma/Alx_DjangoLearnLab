from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

# athentication system url patterens
urlpatterns =  [  
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # Logout view (it will automatically redirect to home page or can be specified)
    path('logout/', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    # Register view
    path('register/', views.register, name='register'),
    # Profile view (uses your custom profile view)
    path('profile/', views.profile, name='profile'),
]

# Post url patterns
urlpatterns += [

    # home views to manage crud operatins for posts
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

# # Comment URL patterns 
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

# search and tags url patterns
urlpatterns += [
    # search view url
    path('posts/search/', views.search_view, name='search'),
    # tags view url
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
]
    
