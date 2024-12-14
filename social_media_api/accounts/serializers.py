from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

#from rest_framework.authtoken.models import Token
#serializers.CharField()
#get_user_model().objects.create_user
#Token.objects.create