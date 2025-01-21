import secrets

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework import status

from posts.models import Post
from users.forms import UserRegistrationForm, CustomLoginForm, UserProfileForm
from users.models import User
from users.email_messages import send_welcome_email


class RegisterView(CreateView):
    '''Форма регистрации с отправкой сообщения на почту'''
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_welcome_email(user, url)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    '''Кастомный логинвью уже со стилями'''
    form_class = CustomLoginForm
    template_name = 'users/login.html'


class ProfileView(LoginRequiredMixin, DetailView):
    '''Контроллер для просмотра профиля'''
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все посты текущего пользователя
        context['posts'] = Post.objects.filter(author=self.request.user).order_by('-created_at')
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['posts'] = Post.objects.filter(author=profile_user).order_by('-created_at')
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер для обновления профиля'''
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'


@login_required
def follow_user(request, user_id):
    """Подписаться на пользователя"""
    target_user = get_object_or_404(User, id=user_id)
    if request.user.is_following(target_user):
        request.user.unfollow(target_user)
        action = 'unfollowed'
    else:
        request.user.follow(target_user)
        action = 'followed'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'action': action, 'followers_count': target_user.followers.count()})
    return HttpResponseRedirect(reverse('users:profile', args=[target_user.id]))


# SERIALIZERS
@method_decorator(csrf_exempt, name='dispatch')
class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(request, username=phone_number, password=password)
        if user:
            return JsonResponse({'message': 'Вход выполнен успешно'}, status=200)
        return JsonResponse({'error': 'Неверный номер телефона или пароль'}, status=401)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
