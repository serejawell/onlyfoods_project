from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from posts.forms import PostCreateForm
from posts.models import Post


class HomePageView(TemplateView):
    template_name = 'posts/hello.html'


class AboutPageView(TemplateView):
    template_name = 'posts/about.html'


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

