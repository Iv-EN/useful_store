from django.core.cache import cache

from .models import Product


def get_product_by_category(category_id):
    """Возвращает все продукты из указанной категории."""
    cache_key = f"product_category_{category_id}"
    products = cache.get(cache_key)
    if products is None:
        products = Product.objects.filter(category_id=category_id)
        cache.set(cache_key, products, 60 * 15)
    return products
