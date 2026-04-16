from django.contrib import admin
from .models import Ad, AdImage


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 3


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    # 1. Убираем поле author из формы редактирования
    exclude = ('author',)

    list_display = ('title', 'category', 'price', 'status', 'created_at')
    list_filter = ('status', 'category')
    inlines = [AdImageInline]

    # 2. Автоматически назначаем автора при сохранении через админку
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Если это новое объявление
            obj.author = request.user
        super().save_model(request, obj, form, change)
