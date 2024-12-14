from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Serializer for registering a new user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Define password as a CharField

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        # Create user using the create_user method
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create a token for the user
        token = Token.objects.create(user=user)
        
        return {
            'user': user,
            'token': token.key
        }
