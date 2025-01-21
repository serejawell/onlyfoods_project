from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from posts.forms import PostCreateForm
from posts.models import Post
from posts.serializers import PostSerializer


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class AboutPageView(TemplateView):
    template_name = 'posts/about.html'

class PostDetailView(DetailView):
    model = Post

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image','is_premium']
    success_url = reverse_lazy('users:profile')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



#Serializers
class PostListAPIView(LoginRequiredMixin, APIView):
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