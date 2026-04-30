from .models import Category


class CategoryService:

    @staticmethod
    def get_category_tree():
        ''

        return Category.objects.filter(parent__isnull=True).prefetch_related('children')
