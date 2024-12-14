from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()

# notification model to truck notifications for post linking or new followers, or new comments
class Notification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor')
    verb = models.TextField(max_length=300)
    target = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'target')
    timestamp = models.DateTimeField(auto_now_add=True)