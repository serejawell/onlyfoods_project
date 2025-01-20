from django.urls import path

from .apps import SubscriptionConfig
from .views import SubscriptionListView, SubscribeView

app_name = SubscriptionConfig.name

urlpatterns = [
    path('subscription/', SubscriptionListView.as_view(), name='subscribe_list'),
    path('<int:subscription_id>/subscribe/', SubscribeView.as_view(), name='subscribe'),
]
