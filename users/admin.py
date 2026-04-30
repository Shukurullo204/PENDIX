from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # тут мы просто регистрируем то что добавили из models
    fieldsets = UserAdmin.fieldsets + (

        ('', {'fields': ('phone', 'avatar', 'city')}),

    )

    add_fieldsets = UserAdmin.add_fieldsets + (

        ('', {'fields': ('phone', 'avatar', 'city')}),

    )

    list_display = ['username', 'email', 'phone', 'city', 'is_staff']
