from django.shortcuts import render
from django.views import View

from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from .models import Subscription
from users.models import User

class SubscriptionListView(ListView):
    """Список подписок"""
    model = Subscription
    context_object_name = 'subscriptions'

class SubscribeView(View):
    """Оформление подписки"""
    def post(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        user = request.user
        if not user.is_authenticated:
            return redirect('users:login')  # Перенаправление на страницу входа

        # Обновление статуса пользователя
        user.is_subscriber = True
        user.save()
        return HttpResponseRedirect(reverse('subscriptions:subscription_list'))