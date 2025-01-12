from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import BlogPostForm
from blog.models import BlogPost


class BlogPostCreateView(CreateView):
    """Представление для создания новой статьи в блоге."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostUpdateView(UpdateView):
    """Представление для редактирования существующей статьи в блоге."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.number_views += 1
        obj.save()
        return obj


class BlogPostListView(ListView):
    """Представление для отображения списка статей в блоге."""

    model = BlogPost
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        """Возвращает только опубликованные записи."""
        return BlogPost.objects.filter(is_published=True).order_by(
            "-created_at"
        )


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
