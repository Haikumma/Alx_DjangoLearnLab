from rest_framework.serializers import ModelSerializer
from .models import Post, Comment

# comment serializer to handle comment data conversion 
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# post serializer to handle post data conversion 
class PostSerializer(ModelSerializer):
    # nested serializer to handle only serialization, it can't handle post and comment creation or updating together
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'