from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Кто написал, кому написал и какая оценка
    list_display = ('author', 'seller', 'rating', 'created_at')
    # Фильтр справа: по дате и по звездам
    list_filter = ('rating', 'created_at')
    # Поиск по тексту отзыва и именам пользователей
    search_fields = ('text', 'author__username', 'seller__username')
    # Чтобы нельзя было случайно накрутить рейтинг из админки (только чтение даты)
    readonly_fields = ('created_at',)
