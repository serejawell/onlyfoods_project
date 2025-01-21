from django.urls import path

from .apps import SubscriptionConfig
from .views import (
    SubscriptionListView,
    CreateCheckoutSessionView,
    PaymentSuccessView,
    PaymentCancelView,
)

app_name = SubscriptionConfig.name

urlpatterns = [
    path('', SubscriptionListView.as_view(), name='subscribe_list'),
    path('checkout/<int:pk>/', CreateCheckoutSessionView.as_view(), name='checkout'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('cancel/', PaymentCancelView.as_view(), name='cancel'),
]