from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя пользоватея',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия пользователя',
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='аватар'
    )
    token = models.CharField(
        max_length=100,
        verbose_name='токен',
        blank=True,
        null=True)
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name="Phone Number"
    )


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



    def __str__(self):
        return str(self.phone_number)
