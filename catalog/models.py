from django.db import models
from django.core.validators import RegexValidator


class Product(models.Model):
    """Описывает продукт."""

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/", verbose_name="Изображение"
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        related_name="products",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата изменения"
    )

    def __str__(self):
        return f"Продукт: {self.name} категория: {self.category.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]


class Category(models.Model):
    """Описывает категорию продукта."""

    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return f"Категория: {self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Contact(models.Model):
    """Описывает информацию о контактном лице."""

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="Телефонный номер необходимо вводить в формате '+9999999999'",
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=12,
        verbose_name="Телефон",
        blank=True
    )
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return f"Контактное лицо: {self.name}, телефон: {self.phone_number}"

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"