from .models import Product


def get_product_by_category(category_id):
    """Возвращает все продукты из указанной категории."""
    return Product.objects.filter(category_id=category_id)
