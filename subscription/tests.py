import pytest
from django.urls import reverse
from subscription.models import Subscription, UserSubscription

@pytest.fixture
def subscription(db):
    return Subscription.objects.create(
        name="Standard Plan",
        description="Basic subscription plan.",
        price=4.99,
        duration_days=30
    )

@pytest.mark.django_db
def test_subscription_creation():
    subscription = Subscription.objects.create(
        name="Premium Plan",
        description="Access to all premium content.",
        price=9.99,
        duration_days=30
    )
    assert Subscription.objects.count() == 1
    assert subscription.name == "Premium Plan"

@pytest.mark.django_db
def test_user_subscription_creation(user, subscription):
    user_subscription = UserSubscription.objects.create(
        user=user,
        subscription=subscription,
        end_date='2025-01-30'
    )
    assert UserSubscription.objects.count() == 1
    assert user_subscription.subscription == subscription

@pytest.mark.django_db
def test_subscription_api(client, user, subscription_factory):
    subscription_factory.create_batch(3)
    url = reverse('subscription:list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 3
