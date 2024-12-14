from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful.', 'token': token.key}, status=status.HTTP_200_OK )
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
           token = Token.objects.get(user=request.user)
           token.delete()
           return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'User is not logged in.'}, status=status.HTTP_400_BAD_REQUEST)
            

    
#Token.objects.create
# Create your views here.
