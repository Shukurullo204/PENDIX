from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    # Видим, какой юзер что лайкнул
    list_display = ('user', 'ad', 'created_at')
    # Поиск по названию товара или имени юзера
    search_fields = ('ad__title', 'user__username')
    # Фильтр по дате добавления в избранное
    list_filter = ('created_at',)
