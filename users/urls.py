from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from users.functions import user_reset_password, email_verification
from users.views import CustomLoginView, ProfileUpdateView, \
    ProfileView, ProfileDetailView, follow_user, RegisterView, LoginView, UserApiView, \
    LoginApiView, RegisterApiView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('password-reset/', user_reset_password, name='password_reset'),
    path('my_profile/', ProfileView.as_view(), name='profile'),
    path('my_profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<int:user_id>/follow/', follow_user, name='follow_user'),

    # API

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterApiView.as_view(), name='register'),
    path('api/login/', LoginApiView.as_view(), name='login'),
    path('api/profile/', UserApiView.as_view(), name='profile'),
]
