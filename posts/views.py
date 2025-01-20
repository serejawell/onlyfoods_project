from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from posts.forms import PostCreateForm
from posts.models import Post
from posts.serializers import PostSerializer


class HomePageView(ListView):
    """Главная страница"""
    model = Post
    template_name = 'posts/hello.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class AboutPageView(TemplateView):
    template_name = 'posts/about.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Возвращает посты только тех, на кого подписан пользователь"""
        user = self.request.user
        if user.is_authenticated:
            # Получаем список пользователей, на которых подписан текущий пользователь
            followed_users = user.following.all()
            # Возвращаем посты этих пользователей, исключая свои
            return Post.objects.filter(author__in=followed_users).exclude(author=user).order_by('-created_at')
        return Post.objects.none()


#Serializers
class PostListAPIView(APIView):
    """
    API для получения списка постов с пагинацией.
    """
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Количество постов на странице
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)