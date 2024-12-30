from django.urls import path
from users.apps import UsersConfig

from users.views import RegisterView, CustomLoginView, ProfileView, ProfileUpdateView, \
 UserListView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
]