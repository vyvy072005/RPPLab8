from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates initial groups and users'

    def handle(self, *args, **kwargs):
            doctor_group, created = Group.objects.get_or_create(name='Doctor')
            admin_group, created = Group.objects.get_or_create(name='Administrator')

            # Создайте или получите существующих пользователей (замените 'username', 'password', 'email')
            doctor_user, created = User.objects.get_or_create(username='doctor1', defaults={'email': 'doctor1@example.com'})
            doctor_user.set_password('password')  # Установите пароль
            doctor_user.save()
            doctor_group.user_set.add(doctor_user)  # Добавьте пользователя в группу

            admin_user, created = User.objects.get_or_create(username='admin1', defaults={'email': 'admin1@example.com'})
            admin_user.set_password('password')
            admin_user.save()
            admin_group.user_set.add(admin_user)

            self.stdout.write(self.style.SUCCESS('Successfully created groups and users'))