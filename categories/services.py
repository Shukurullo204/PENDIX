from .models import Category

class CategoryService:
    @staticmethod
    def get_category_tree():
        """Возвращает только корневые категории с предзагруженными детьми"""
        return Category.objects.filter(parent__isnull=True).prefetch_related('children')
