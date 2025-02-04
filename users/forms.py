from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.functions import clean_phone_number
from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    """Форма создания нового пользователя."""

    phone_number = forms.CharField(
        max_length=12,
        required=False,
        help_text="Введите номер телефона (не обязательно).",
    )

    class Meta:
        model = MyUser
        fields = (
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр."
            )
        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Имя пользователя",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Электронная почта",
            }
        )
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Телефон. Не обязательно",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите пароль",
            }
        )


class MyUserChangeForm(forms.ModelForm):
    """Форма изменения информации о пользователе."""

    class Meta:
        model = MyUser
        fields = ("username", "email", "phone_number", "avatar", "country")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр."
            )
        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Имя пользователя",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Электронная почта",
            }
        )
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Телефон",
            }
        )
        self.fields["avatar"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Фото",
            }
        )
        self.fields["country"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Страна",
            }
        )
