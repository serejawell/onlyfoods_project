# Generated by Django 4.2.2 on 2025-01-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=2, max_length=20, verbose_name='Никнейм'),
            preserve_default=False,
        ),
    ]
