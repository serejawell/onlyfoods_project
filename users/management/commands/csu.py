from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create superuser and admin group'

    def handle(self, *args, **options):
        User = get_user_model()

        # Создание группы "admin"
        admin_group, created = Group.objects.get_or_create(name='admin')

        # Создание суперпользователя
        user = User.objects.create(
            email='admin@example.com',  # укажите нужный email
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('1234')  # установите нужный пароль
        user.groups.add(admin_group)  # Добавление пользователя в группу "admin"
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created superuser with email: {user.email}, password: 1234.'
        ))