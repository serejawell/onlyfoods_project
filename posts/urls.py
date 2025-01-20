from django.urls import path
from posts.apps import PostsConfig
from posts.views import HomePageView, AboutPageView, PostCreateView, PostListView, PostListAPIView

app_name = PostsConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('welcome/', HomePageView.as_view(), name='base'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('api/posts/', PostListAPIView.as_view(), name='posts_api'),
]
