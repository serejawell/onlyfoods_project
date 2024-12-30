import secrets

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegistrationForm
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
        url = f'http://{host}/account/email-confirm/{token}'
        send_welcome_email(user, url)
        return super().form_valid(form)