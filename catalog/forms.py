from django import forms
from django.contrib.auth import get_user_model

from .models import Product

User = get_user_model()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def clean_image(self):
        """Проверка, что файл является изображением."""
        image = self.cleaned_data.get("image")
        if image and not image.name.endswith(("jpg", "jpeg", "png", "gif")):
            raise forms.ValidationError(
                "Изображение должно быть в формате JPG, JPEG, PNG или GIF."
            )
        return image
