import requests
# Получение категорий
# Получение подробной информации о товаре


def get_product_details(product_id):
    response = requests.get(f'http://gambitcorporation.ru:8000/api/products/{product_id}/')
    if response.status_code == 200:
        return response.json()
    return None


def get_categories():
    response = requests.get('http://gambitcorporation.ru:8000/api/categories/')
    if response.status_code == 200:
        return response.json()
    return []


def get_products(category_id):
    response = requests.get(f'http://gambitcorporation.ru:8000/api/products/?category={category_id}')
    if response.status_code == 200:
        return response.json()
    return []