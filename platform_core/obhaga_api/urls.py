from django.urls import path
from .views import CategoryListView, ProductListView, Product

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
]
