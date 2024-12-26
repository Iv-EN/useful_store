import json
import os.path
import logging

from django.conf import settings
from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Загрузка данных из json файла."

    @staticmethod
    def clear_models(model):
        """Очистка всех записей в указанной модели."""
        model.objects.all().delete()

    @staticmethod
    def set_sequence(model):
        """Установить последовательность автоинкремента на max_id + 1."""
        table_name = model._meta.db_table
        max_id = model.objects.all().order_by("-id")[0].id
        sequence_sql = (
            f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH {max_id + 1}"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(sequence_sql)
        except Exception as e:
            logger.error(
                f"При сбросе нумерации `id` для {model.__name__} произошла ошибка: {e}"
            )

    @staticmethod
    def get_json_file(filename):
        """Получение пути к json файлу."""
        file_path = os.path.join(settings.BASE_DIR, "fixtures", filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл {filename} не найден.")
        return file_path

    def handle(self, *args, **options):
        models = [Product, Category]
        for model in models:
            self.clear_models(model)

        fixture_file = self.get_json_file("catalog_data.json")
        with open(fixture_file, "r", encoding="utf-16") as file:
            fixtures = json.load(file)

        categories = []
        products = []

        for fixture in fixtures:
            model_name = fixture["model"]
            pk = fixture["pk"]
            fields = fixture["fields"]
            if model_name == "catalog.category":
                categories.append(Category(pk=pk, **fields))
            elif model_name == "catalog.product":
                products.append({"pk": pk, "fields": fields})

        try:
            Category.objects.bulk_create(categories)
            logger.info(f"{len(categories)} категорий занесено в базу")
            product_objects = []
            for products_data in products:
                pk = products_data["pk"]
                fields = products_data["fields"]
                category_id = fields.pop("category")
                fields["category"] = Category.objects.get(pk=category_id)
                product_objects.append(Product(pk=pk, **fields))
            Product.objects.bulk_create(product_objects)
            logger.info(f"{len(product_objects)} продуктов занесено в базу")
        except Exception as e:
            logger.error(f"Произошла ошибка при загрузке данных: {e}")

        for model in models:
            self.set_sequence(model)
