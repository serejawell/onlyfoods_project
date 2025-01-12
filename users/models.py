from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия пользователя',
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание автора'
    )
    stripe_account_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Stripe Account ID'
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name="Телефон"
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone_number)


