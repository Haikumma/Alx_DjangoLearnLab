from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CommentSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from .models import Comment, Post


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']