from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserAPIView, FollowView


urlpatterns = [
    # athentication url paths
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    
    # user profile management url paths
    path('profile/<username>', UserAPIView.as_view(), name='profile'),

    # following url paths
    path('follow/<username>', FollowView.as_view({'post':'follow'}), name='follow'),
    path('unfollow/<username>', FollowView.as_view({'delete':'unfollow'}), name='unfollow'),
    # "follow/<int:user_id>"
    # "unfollow/<int:user_id>/"
]