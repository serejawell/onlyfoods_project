from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    nickname = models.CharField(
        max_length=20,
        verbose_name='Никнейм'
    )
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
    followers = models.ManyToManyField(
        'self',  # Связь с той же моделью
        symmetrical=False,  # Симметричная связь не нужна (подписки и подписчики различаются)
        related_name='following',  # Название обратной связи (список, на кого подписан пользователь)
        blank=True,
        null=True,
        verbose_name='Подписчики'
    )
    is_subscriber = models.BooleanField(
        default=False,
        verbose_name='Подписка'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def posts_count(self):
        return self.posts.count()

    def followers_count(self):
        """Возвращает количество подписчиков"""
        return self.followers.count()

    def following_count(self):
        """Возвращает количество подписок"""
        return self.following.count()

    def follow(self, user):
        """Подписаться на пользователя"""
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        """Отписаться от пользователя"""
        if user != self:
            self.following.remove(user)

    def is_following(self, user):
        """Проверить, подписан ли текущий пользователь на другого"""
        return self.following.filter(id=user.id).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone_number)
