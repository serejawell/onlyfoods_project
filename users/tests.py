import pytest
from django.urls import reverse
from users.models import User

@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        phone_number='+123456789',
        password='password123',
        first_name='Test',
        last_name='User'
    )

@pytest.mark.django_db
def test_user_registration(client):
    url = reverse('users:register')
    data = {
        'phone_number': '+123456789',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful registration
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_user_login(client, user):
    url = reverse('users:login')
    data = {'phone_number': user.phone_number, 'password': 'password123'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_user_profile_view(client, user):
    client.force_login(user)
    url = reverse('users:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user'] == user
