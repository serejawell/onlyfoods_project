from django.db import models
from users.models import User

class Subscription(models.Model):
    """Модель подписки"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название подписки'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание подписки'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена подписки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.name} - {self.price}₽"



