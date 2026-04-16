from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True,     # ← ДОБАВЬ
        null=True,      # ← ДОБАВЬ
        default=None    # ← ДОБАВЬ
    )
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'