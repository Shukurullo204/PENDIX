from django.contrib import admin

from .models import Category



@admin.register(Category)

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}                                    

    list_display = ['name', 'parent', 'slug']

    search_fields = ['name']

