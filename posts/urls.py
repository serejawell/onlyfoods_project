from django.urls import path
from posts.apps import PostsConfig
from posts.views import AboutPageView, PostCreateView, PostListView, PostListAPIView, PostUpdateView, \
    PostDeleteView, PostDetailView

app_name = PostsConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('api/posts/', PostListAPIView.as_view(), name='posts_api'),
]
