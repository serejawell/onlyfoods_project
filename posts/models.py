from django.db import models

from users.models import User


class Post(models.Model):
    """Модель поста"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Контент'
    )
    image = models.ImageField(
        upload_to='posts/images',
        verbose_name='Изображение'
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name='Премиум контент'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

