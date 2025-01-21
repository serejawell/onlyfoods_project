import stripe
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, redirect

from onlyfoods import settings
from .models import Subscription, UserSubscription
from users.models import User




class SubscriptionListView(ListView):
    """Список доступных подписок"""
    model = Subscription
    context_object_name = 'subscriptions'


from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe
from .models import Subscription

class CreateCheckoutSessionView(View):
    """Создание платежной сессии Stripe"""
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription_id = kwargs['pk']
        subscription = get_object_or_404(Subscription, id=subscription_id)

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
            success_url=request.build_absolute_uri('/success/'),  # URL при успешной оплате
            cancel_url=request.build_absolute_uri('/cancel/'),  # URL при отмене
        )

        # Перенаправление пользователя на страницу оплаты
        return redirect(session.url)



class PaymentSuccessView(View):
    """Обработка успешного платежа"""
    def get(self, request):
        # Найти пользователя и добавить ему подписку
        user = request.user
        subscription_id = request.GET.get('subscription_id')  # Передайте ID подписки через параметры
        subscription = get_object_or_404(Subscription, id=subscription_id)

        # Создать запись о подписке
        UserSubscription.objects.create(
            user=user,
            subscription=subscription
        )

        return render(request, 'subscriptions/success.html')


class PaymentCancelView(View):
    """Обработка отмены платежа"""
    def get(self, request):
        return render(request, 'subscriptions/cancel.html')
