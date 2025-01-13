from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(APIView):
    def get(self, request):
        category_id = request.query_params.get('id')  # Получаем параметр 'id' из запроса

        if category_id:
            try:
                category = Category.objects.get(id=category_id)  # Ищем категорию по id
                serializer = CategorySerializer(category)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()  # Если 'id' не передан, возвращаем все категории
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)


class ProductListView(APIView):
    def get(self, request):
        # Получаем параметр 'category' из запроса
        category_id = request.query_params.get('category')

        # Если параметр category существует, фильтруем товары по категории
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                products = Product.objects.filter(category=category)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        elif 'id' in request.query_params:
            # Получаем товар по id
            product_id = request.query_params.get('id')
            try:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Если параметра 'category' нет, возвращаем все товары
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)