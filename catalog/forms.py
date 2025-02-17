from django import forms
from django.contrib.auth import get_user_model
from PIL import Image

from .models import Product

User = get_user_model()


class ProductForm(forms.ModelForm):
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "category",
            "price",
            "is_published",
        ]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите название продукта",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите описание продукта",
            }
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["category"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите цену продукта",
            }
        )
        self.fields["is_published"].widget.attrs.update(
            {
                "class": "form-check-input",
                "placeholder": "Опубликовать на сайте",
            }
        )

    def clean_name(self):
        """Проверка на наличие запрещенных слов в названии."""
        name = self.cleaned_data.get("name")
        if any(word in name.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError(
                "Название продукта содержит запрещенные слова."
            )
        return name

    def clean_description(self):
        """Проверка на наличие запрещенных слов в описании."""
        description = self.cleaned_data.get("description")
        if any(word in description.lower() for word in self.FORBIDDEN_WORDS):
            raise forms.ValidationError(
                "Описание продукта содержит запрещенные слова."
            )
        return description

    def clean_image(self):
        """Проверка, что файл является изображением."""
        image = self.cleaned_data.get("image")
        if image:
            try:
                img = Image.open(image)
                img.verify()
            except Exception:
                raise forms.ValidationError("Файл не является изображением.")
            if not image.name.endswith(("jpeg", "png")):
                raise forms.ValidationError(
                    "Изображение должно быть в формате JPEG или PNG."
                )
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Изображение не должно превышать 5MB."
                )
        return image

    def clean_price(self):
        """Проверка, что цена является не отрицательным числом."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
