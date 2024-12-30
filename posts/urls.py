from django.urls import path
from posts.apps import PostsConfig
from posts.views import HomePageView


app_name = PostsConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='base'),
    ]