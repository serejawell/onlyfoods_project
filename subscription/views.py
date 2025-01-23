from django.urls import reverse
from django.conf import settings
import stripe
from django.views.generic import ListView, RedirectView
from onlyfoods import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from datetime import timedelta
from .models import Subscription, UserSubscription


class SubscriptionListView(ListView):
    """Список доступных подписок"""
    model = Subscription
    context_object_name = 'subscriptions'


class CreateCheckoutSessionView(View):
    """Создание платежной сессии Stripe"""
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription_id = kwargs['pk']
        subscription = get_object_or_404(Subscription, id=subscription_id)

        # Генерируем URL для success с передачей subscription_id
        success_url = request.build_absolute_uri(
            reverse('subscription:success') + f"?subscription_id={subscription.id}"
        )
        cancel_url = request.build_absolute_uri(reverse('subscription:cancel'))

        # Создание платежной сессии
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': subscription.name,
                    },
                    'unit_amount': int(subscription.price * 100),  # Stripe принимает сумму в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,  # Указываем правильный URL
            cancel_url=cancel_url,  # URL при отмене
        )

        return redirect(session.url)








class PaymentSuccessView(LoginRequiredMixin, View):
    """Обработка успешного платежа"""
    def get(self, request):
        user = request.user
        subscription_id = request.GET.get('subscription_id')  # Берём ID подписки из URL

        if not subscription_id:
            return render(request, 'subscription/error.html', {'message': 'Ошибка: Подписка не найдена'})

        # Получаем подписку
        subscription = get_object_or_404(Subscription, id=subscription_id)

        # Создаём запись о подписке
        UserSubscription.objects.create(
            user=user,
            subscription=subscription,
            start_date=now(),
            end_date=now() + timedelta(days=subscription.duration_days)
        )

        # Делаем пользователя премиумным
        user.is_premium = True
        user.save()

        return render(request, 'subscription/success.html', {'subscription': subscription})


        # Обновляем статус пользователя
        user.is_premium = True
        user.save()

        return render(request, 'subscriptions/success.html', {'subscription': subscription})



class PaymentCancelView(View):
    """Обработка отмены платежа"""
    def get(self, request):
        return render(request, 'subscriptions/cancel.html')
