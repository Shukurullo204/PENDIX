from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем наши поля в админку
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация', {'fields': ('phone', 'avatar', 'city')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Доп. информация', {'fields': ('phone', 'avatar', 'city')}),
    )
    list_display = ['username', 'email', 'phone', 'city', 'is_staff']
