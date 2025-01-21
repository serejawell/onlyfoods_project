from django.db import models
from django.utils.timezone import now
from datetime import timedelta
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
    duration_days = models.PositiveIntegerField(
        verbose_name='Длительность подписки (в днях)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.name} - {self.price}$ на {self.duration_days} дней"


class UserSubscription(models.Model):
    """Модель подписки пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_subscriptions',
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='user_subscriptions',
        verbose_name='Подписка'
    )
    start_date = models.DateTimeField(
        default=now,
        verbose_name='Дата начала'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания'
    )

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def save(self, *args, **kwargs):
        """Автоматически устанавливает дату окончания подписки"""
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.subscription.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Подписка {self.user} на {self.subscription.name}"


class Payment(models.Model):
    """Модель для платежей"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Подписка'
    )
    stripe_charge_id = models.CharField(
        max_length=100,
        verbose_name='ID платежа Stripe'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата платежа'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"Платеж {self.id} от {self.user} на сумму {self.amount}$"
