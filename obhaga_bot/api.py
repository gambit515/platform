import requests
# Получение категорий
# Получение подробной информации о товаре
print(f'http://django_container:8000/api/products/?id={1}')
response = requests.get(f'http://django_container:8000/api/products/?id={1}')

def get_product_details(product_id):
    response = requests.get(f'http://web:8000/api/products/?id={product_id}')
    if response.status_code == 200:
        return response.json()
    return None

def get_categories():
    response = requests.get('http://web:8000/api/categories/')
    if response.status_code == 200:
        return response.json()
    return []

def get_products(category_id):
    response = requests.get(f'http://web:8000/api/products/?category={category_id}')
    if response.status_code == 200:
        return response.json()
    return []