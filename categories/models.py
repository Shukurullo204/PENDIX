from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)

    def __str__(self):
        # Если есть родитель, покажем структуру: "Электроника > Смартфоны"
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"