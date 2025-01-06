import requests

host = 'web'
def get_categories():
    response = requests.get(f'http://{host}:8000/api/categories/')
    if response.status_code == 200:
        return response.json()
    return []


def get_category_by_id(category_id):
    response = requests.get(f'http://{host}:8000/api/categories/?id={category_id}')
    if response.status_code == 200:
        return response.json()
    return None


def get_products_by_category(category_id):
    response = requests.get(f'http://{host}:8000/api/products/?category={category_id}')
    if response.status_code == 200:
        return response.json()
    return []

def get_product_by_id(product_id):
    response = requests.get(f'http://{host}:8000/api/products/?id={product_id}')
    if response.status_code == 200:
        return response.json()
    return None
