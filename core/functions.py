from django import forms


def clean_phone_number(self):
    phone_number = self.cleaned_data.get("phone_number")
    if phone_number and not phone_number.isdigit():
        raise forms.ValidationError(
            "Номер телефона должен состоять только из цифр."
        )
    return phone_number
