from django.views.generic import ListView
from .models import Category

class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Показываем только верхний уровень, детей подгрузим в шаблоне
        return Category.objects.filter(parent__isnull=True)
