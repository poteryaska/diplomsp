from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='lemanove@gmail.com',
            phone='+71234567802',
            first_name='Evgeniia',
            last_name='Lemanova',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('12345678')
        user.save()