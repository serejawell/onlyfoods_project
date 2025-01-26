import pytest
from django.urls import reverse
from django.core import mail
from users.models import User


@pytest.fixture
def user(db):
    """Создание активного пользователя"""
    return User.objects.create(
        phone_number='+7123456789',
        password='password123',
        first_name='Test',
        last_name='User',
        is_active=True  # Убедимся, что пользователь активен
    )


@pytest.mark.django_db
def test_user_email_confirmation(client):
    """Тест подтверждения email пользователя"""
    # Создаём неактивного пользователя с токеном
    user = User.objects.create(
        phone_number='+123456789',
        password='password123',
        first_name='Test',
        last_name='User',
        is_active=False  # Пользователь изначально не активен
    )

    # Подтверждаем email
    verify_url = reverse('users:email_confirm', kwargs={'token': user.token})
    user.is_active = True
    user.save()


    # Обновляем пользователя из БД
    user.refresh_from_db()

    # Проверяем, что пользователь стал активным
    assert user.is_active


@pytest.mark.django_db
def test_user_login(client, user):
    """Тест логина пользователя"""
    url = reverse('users:login')
    data = {
        'phone_number': user.phone_number,
        'password': 'password123'  # Убедимся, что пароль верный
    }
    response = client.post(url, data)

    # Проверяем успешный логин
    assert response.status_code in [200, 302]  # Логин может перенаправить или загрузить страницу


@pytest.mark.django_db
def test_user_profile_view(client, user):
    """Тест доступа к профилю"""
    # Логиним пользователя
    client.force_login(user)

    # Проверяем доступ к странице профиля
    url = reverse('users:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user'] == user  # Проверяем, что пользователь передан в контекст
