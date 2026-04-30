from django.contrib import admin

from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'created_at')

    search_fields = ('ad__title', 'user__username')

    list_filter = ('created_at',)
