from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаемые поля в списке
    search_fields = ('name',)  # Поле поиска


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'in_stock', 'category')  # Поля для отображения
    list_filter = ('in_stock', 'category')  # Фильтры справа
    search_fields = ('name', 'description')  # Поля для поиска
