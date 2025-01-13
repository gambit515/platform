from django.shortcuts import render
from obhaga_api.models import Product, Category

def Product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        selected_category = Category.objects.get(id=category_id)
    else:
        products = Product.objects.all()
        selected_category = None

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'product_list.html', context)