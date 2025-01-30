from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import BlogPost

User = get_user_model()


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите заголовок",
            }
        )
        self.fields["content"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите текст статьи",
                "rows": 10,
            }
        )
        self.fields["preview"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Выберите изображение",
            }
        )
        self.fields["is_published"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )
