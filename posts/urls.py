from django.urls import path
from posts.apps import PostsConfig
from posts.views import HomePageView, AboutPageView, PostCreateView

app_name = PostsConfig.name

urlpatterns = [
    path('welcome/', HomePageView.as_view(), name='base'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('create/', PostCreateView.as_view(), name='create'),
    ]