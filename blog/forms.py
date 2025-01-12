from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import BlogPost

User = get_user_model()


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published"]
