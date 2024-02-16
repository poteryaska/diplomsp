from django.db import models
from django.contrib.auth.models import AbstractUser
from users.utils import create_digit_code
from django.core.validators import MinLengthValidator, MaxLengthValidator

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=40, verbose_name='имя пользователя', unique=True)
    password = models.CharField(max_length=20, verbose_name='пароль')
    phone = models.CharField(max_length=12, verbose_name='телефон', unique=True)
    referral_code = models.CharField(max_length=6, null=True, default=None)
    else_referral_code = models.CharField(
        max_length=6,
        validators=[MinLengthValidator(limit_value=6), MaxLengthValidator(limit_value=6)],
        **NULLABLE,
    )
    activated = models.BooleanField(default=False)  # для проверки введен ли else_referral_code
    code = models.CharField(max_length=4, blank=True)

    # Заполнениe поля code
    def save(self, *args, **kwargs):
        self.code = create_digit_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'