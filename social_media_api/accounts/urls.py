# accounts/urls.py
from django.urls import path
from .views import RegisterSerializerView, LoginView

urlpatterns = [
    path('register/', RegisterSerializerView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

