from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# from rest_framework.authtoken.models import Token
# serializers.CharField()
# serializers.CharField()
# get_user_model().objects.create_user
# Token.objects.create

# serializer to handle user data conversion (serializing and deserializing)
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

           