from django.db import models
from django.conf import settings
from categories.models import Category
from django.core.validators import MinLengthValidator


class Ad(models.Model):
    STATUS_CHOICES = (('active', 'Активно'), ('sold', 'Продано'), ('archived', 'Архив'))
    CURRENCY_CHOICES = (('UZS', 'сум'), ('USD', '$'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='ads')

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(
        validators=[MinLengthValidator(80, message="Минимум 80 символов")],
        verbose_name="Описание"
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS', verbose_name="Валюта")
    phone = models.CharField(max_length=20, verbose_name="Контактный номер")

    # Поля для карты
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads/photos/')