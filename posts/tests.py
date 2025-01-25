import pytest
from django.urls import reverse
from subscription.models import Subscription, UserSubscription
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        phone_number='+123456789',
        password='password123',
        first_name='Test',
        last_name='User',
        nickname='testuser'
    )


@pytest.fixture
def subscription(db):
    return Subscription.objects.create(
        name="Premium Plan",
        description="Access to all premium content.",
        price=9.99,
        duration_days=30
    )


@pytest.mark.django_db
def test_subscription_creation():
    """Тест создания подписки"""
    subscription = Subscription.objects.create(
        name="Standard Plan",
        description="Basic subscription plan.",
        price=4.99,
        duration_days=30
    )
    assert Subscription.objects.count() == 1
    assert subscription.name == "Standard Plan"


@pytest.mark.django_db
def test_user_subscription_creation(user, subscription):
    """Тест подписки пользователя"""
    user_subscription = UserSubscription.objects.create(
        user=user,
        subscription=subscription
    )
    assert UserSubscription.objects.count() == 1
    assert user_subscription.subscription == subscription


@pytest.mark.django_db
def test_subscription_api(client, user, subscription):
    """Тест API получения списка подписок"""
    url = reverse('subscription:subscribe_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['subscriptions']) >= 1
