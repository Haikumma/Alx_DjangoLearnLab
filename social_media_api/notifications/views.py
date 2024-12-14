from django.contrib.contenttypes.models import ContentType
from posts.models import Like, Comment, Post
from .models import Notification
from rest_framework.generics import ListAPIView
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from django.contrib.auth import get_user_model
User = get_user_model()

VERB_TEMPLATES = {
    'like': 'new post like',
    'comment': 'new comment',
    'follow': 'new follower'
}

def perform_notification_creation(recipient, actor, target, like_content_type, verb):
    """Handles notification creation with specified parameters."""
    Notification.objects.create(content_type=like_content_type,
                                                   recipient=recipient, 
                                                    actor=actor,
                                                    verb=verb,
                                                    target=target,
                                                    )
    
def generating_notification(model, recipient, actor, target):
    """Determines the notification type and generates it based on the model."""
    if model == Like:
        content_type = ContentType.objects.get_for_model(Like)
        verb = VERB_TEMPLATES['like']
    elif model == Comment:
        content_type = ContentType.objects.get_for_model(Post)
        verb = VERB_TEMPLATES['comment']
    elif model == User:
        content_type = ContentType.objects.get_for_model(User)
        verb = VERB_TEMPLATES['follow']
    else:
        raise ValueError(f"Unsupported model type: {model}")
    
    perform_notification_creation(recipient, actor, target, content_type, verb)

class NotificationView(ListAPIView):
    """Fetches user notifications created in the past 24 hours."""
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Filter notifications by recipient and date range
        notifications = self.queryset.filter(
            recipient=request.user,
            timestamp__date__gte=yesterday,
            timestamp__date__lte=today
        )
        
        # Paginate results for scalability
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_paginated_response(
                NotificationSerializer(page, many=True).data
            )
            return serializer
        
        # Return notifications or no-content response
        serializer = NotificationSerializer(notifications, many=True)
        if notifications.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No notifications found'}, status=status.HTTP_204_NO_CONTENT)

        
        
        