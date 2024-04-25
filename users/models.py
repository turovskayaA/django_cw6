from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    token = models.CharField(max_length=10, verbose_name='Верификация', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_is_active', 'Может блокировать пользователей')
        ]
