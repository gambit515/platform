from django.urls import path
from .views import Product_list

urlpatterns = [
    path('', Product_list, name='product_list'),
    path('category/<int:category_id>/', Product_list, name='product_list_by_category'),
]