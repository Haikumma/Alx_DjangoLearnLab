from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import UserSerializer
from .permission import IsLoggedIn
from rest_framework import status
from .models import CustomUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import GenericViewSet
from notifications.views import generating_notification
User = get_user_model()

# register view to handle user creation
class RegisterView(APIView):

    def post(self, request):
        
        """
        Handle the creation of a new user.

        Args:
            request (Request): The request body with the user details.

        Returns:
            Response: A response with the result of the registration.

        Raises:
            Exception: If the registration of the user failed.
        """
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        profile_picture = request.data.get('profile_picture', None)
        bio = request.data.get('bio', '')

        if not username or not email or not password:
            return Response({'error': 'Username, Email, Password, are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture,
                bio=bio
            )
            return Response({'message':'User registered successfully.'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# login view to handle credentials validation and token generation
class LoginView(APIView):  

    def post(self, request):
        """
        Handle the login of a user.

        Args:
            request (Request): The request body with the user credentials.

        Returns:
            Response: A response with the result of the login and token.

        Raises:
            Exception: If the login of the user failed.
        """

        username = request.data.get('username') 
        password = request.data.get('password') 

        if not username and not password:
            return Response({'error':'Username and Password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request=request, username=username, password=password)

        if user is not None:

            token, created = Token.objects.get_or_create(user=user)
            return Response(
                        {
                            'message': 'Login successful', 
                            'token': token.key
                        }, 
                            status=status.HTTP_200_OK 
                        )
        
        return Response({'error':'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

# logout view to handle logout operation and token deletion
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle the logout of a user by deleting the authentication token.

        Args:
            request (Request): The request object containing the user information.

        Returns:
            Response: A response indicating the success or failure of the logout operation.
        """

        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message':'Logout seccussful'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

# user viewset to handle profile managment(reterive, update, delete)
# note : user creation handled in RegisterView
class UserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsLoggedIn]
    lookup_field = 'username'

    def get_object(self):
        """
    Retrieve and return the user object based on the username lookup field.

    Checks the permissions for the retrieved object before returning it.

    Returns:
        User: The user object if permissions are granted and the object is found.
        """
        obj =  super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def destroy(self, request, *args, **kwargs):
        """
    Custom destroy method to return a 200 status code with a success message
    instead of the default 204 status code with an empty response.

    Args:
        request: The request object
        *args: Additional positional arguments
        **kwargs: Additional keyword arguments

    Returns:
        Response: A response with a success message and a 200 status code
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Deleted successfully."}, 
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """
        Destroy the given user object.

        Args:
            instance: The user object to be deleted
        """
        instance.delete()

# FollowView handle following and unfollowing custom  operations 
# note: when I am about to run the api switch from generics.CreateAPIView to GenericViewSet
class FollowView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=['POST'], detail=True, url_path='follow')
    def follow(self, request, username=None):
        """
    Handle the follow operation for a user.

    Allows a user to follow another user identified by the username.

    Args:
        request (Request): The request object containing the user information.
        username (str): The username of the user to be followed.

    Returns:
        Response: A response indicating the success or failure of the follow operation.
                  On success, returns a message with HTTP 200 status.
                  On failure, returns an error message with HTTP 400 status.
        """
        try: 
            followed_user = self.queryset.get(username=username)
        except self.queryset.model.DoesNotExist as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

        if request.user == followed_user:
            return Response({'error': "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=followed_user.id).exists():
            return Response({'error': "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)    
        
        request.user.following.add(followed_user)
        
        generating_notification(User, followed_user, request.user, followed_user.id)
        return Response({'message': 'Follow seccussful'}, status=status.HTTP_200_OK)
    
    @action(methods=['DELETE'], detail=True, url_path='unfollow')
    def unfollow(self, request, username):
        """
    Handle the unfollow operation for a user.

    Allows a user to unfollow another user identified by the username.

    Args:
        request (Request): The request object containing the user information.
        username (str): The username of the user to be unfollowed.

    Returns:
        Response: A response indicating the success or failure of the unfollow operation.
                  On success, returns a message with HTTP 200 status.
                  On failure, returns an error message with HTTP 400 status.
        """
        try:
            followed_user = self.queryset.get(username=username)
        except self.queryset.model.DoesNotExist:
                return Response({'error': "The specified user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user == followed_user:
            return Response({'error': "You can't unfollow yourself because by default you can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(id=followed_user.id).exists():
            return Response({'error': "You don't follow this user"}, status=status.HTTP_400_BAD_REQUEST) 
        
        request.user.following.remove(followed_user.id)
        return Response({'message': "Unfollow seccussful"}, status=status.HTTP_200_OK) 
    