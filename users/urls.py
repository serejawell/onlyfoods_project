from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig

from users.functions import user_reset_password, email_verification
from users.views import RegisterView, CustomLoginView, ProfileUpdateView, \
    UserListView, UserDetailView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('password-reset/', user_reset_password, name='password_reset'),
    path('my_profile/', ProfileView.as_view(), name='profile'),
    path('my_profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
