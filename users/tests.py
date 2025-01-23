import pytest
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
def test_user_registration(client):
    """Тест регистрации пользователя"""
    url = reverse('users:register')
    data = {
        'phone_number': '+123456789',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'nickname': 'testuser'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Проверка редиректа после успешной регистрации
    assert User.objects.count() == 1


@pytest.fixture
def user(db):
    """Фикстура для создания пользователя"""
    return User.objects.create_user(
        phone_number='+123456789',
        password='password123',
        first_name='Test',
        last_name='User',
        nickname='testuser'
    )


@pytest.mark.django_db
def test_user_login(client, user):
    """Тест логина"""
    url = reverse('users:login')
    data = {'phone_number': user.phone_number, 'password': 'password123'}
    response = client.post(url, data)
    assert response.status_code in [200, 302]
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_user_profile_view(client, user):
    """Тест просмотра профиля"""
    client.force_login(user)
    url = reverse('users:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user'] == user
