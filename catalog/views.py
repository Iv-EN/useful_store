from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from .forms import ProductForm
from .models import Category, Contact, Product
from .services import get_product_by_category

PRODUCT_PER_PAGE = 8
"""Количество продуктов отображаемых на странице."""


class ProductListView(ListView):
    """
    Представление для отображения списка продуктов с постраничной навигацией.
    """

    model = Product
    paginate_by = PRODUCT_PER_PAGE

    def get_queryset(self):
        """Возвращает продукты в зависимости от статуса пользователя."""
        user = self.request.user
        cache_key = f"product_list_{user.id if user.is_authenticated else 'quest'}_cache"
        queryset = cache.get(cache_key)
        if queryset is None:
            if user.is_authenticated:
                queryset = Product.objects.filter(
                    Q(is_published=True) | Q(owner=user)
                ).order_by("-created_at")
            else:
                queryset = Product.objects.filter(is_published=True).order_by(
                    "-created_at"
                )
            cache.set(cache_key, queryset, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ContactView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка контактов
    с формой для отправки сообщений.
    """

    model = Contact
    template_name = "catalog/contacts.html"

    def post(self, request):
        """Отправка сообщения из формы."""
        user_name = request.POST.get("name")
        phone = request.POST.get("phone")
        user_message = request.POST.get("message")
        filename = f"сообщение_от_{user_name}.txt"
        message = f"""
            Пользователь: {user_name} (телефон: {phone})
            оставил сообщение: '{user_message}'"""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(message)
        return redirect("catalog:contacts")


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения детальной информации о продукте."""

    model = Product


class ProductView(LoginRequiredMixin, View):
    """Представление для создания и редактирования продукта."""

    FIELDS_TO_POP = ["name", "description", "image", "category", "price"]
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_form_and_title(self, pk):
        """Возвращает форму и заголовок для продукта."""
        if pk:
            product = get_object_or_404(self.model, pk=pk)
            title = "Редактировать продукт"
        else:
            product = None
            title = "Создать продукт"
        return product, title

    def has_permission(self, product, user):
        """Проверяет права доступа к продукту."""
        if product.owner == user:
            return True
        return user.has_perm("catalog.can_unpublish_product")

    def get(self, request, pk=None):
        """Отображает форму создания или редактирования продукта."""
        product, title = self.get_form_and_title(pk)
        can_unp = request.user.has_perm("catalog.can_unpublish_product")
        if product:
            if not self.has_permission(product, request.user):
                raise PermissionDenied()
            if product.owner == request.user:
                form = self.form_class(instance=product)
            elif can_unp:
                form = self.form_class(instance=product)
                for field in self.FIELDS_TO_POP:
                    form.fields.pop(field, None)
            else:
                raise PermissionDenied()
        else:
            form = self.form_class()
        return render(
            request,
            self.template_name,
            {"form": form, "title": title, "can_unp": can_unp},
        )

    def get_object(self, pk):
        """Возвращает продукт по его pk."""
        return get_object_or_404(Product, pk=pk)

    def create_product(self, request):
        """Обрабатывает запрос на создание продукта."""
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            message = "Продукт создан."
            messages.info(request, message)
            return redirect("catalog:product_detail", pk=product.pk)
        return render(
            request,
            self.template_name,
            {"form": form, "title": "Создать продукт"},
        )

    def update_product(self, request, product):
        """Обрабатывает запрос на редактирование продукта."""
        if self.has_permission(product, request.user):
            form = self.form_class(
                request.POST, request.FILES, instance=product
            )
            if form.is_valid():
                product.save()
                message = "Продукт изменён."
                messages.info(request, message)
                return redirect("catalog:product_detail", pk=product.pk)
        return render(
            request,
            self.template_name,
            {"form": form, "title": "Редактировать продукт"},
        )

    def post(self, request, pk=None):
        """Обрабатывает запрос на создание или редактирование продукта."""
        if pk:
            product = self.get_object(pk)
            return self.update_product(request, product)
        else:
            return self.create_product(request)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление для удаления продукта."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def test_func(self):
        """Проверяет права доступа к продукту."""
        product = self.get_object()
        return (
            product.owner == self.request.user
            or self.request.user.groups.filter(
                name="Модератор продуктов"
            ).exists()
        )

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права доступа перед удалением."""
        product = self.get_object()
        if (
            not self.request.user.has_perm("catalog.can_unpublish_product")
            and product.owner != request.user
        ):
            messages.error(
                self.request, "У вас недостаточно прав для удаления продукта."
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт."""
        messages.success(request, "Продукт успешно удален.")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        """Обрабатывает отсутствие прав у пользователя."""
        messages.error(
            self.request, "У вас недостаточно прав для удаления продукта."
        )
        return super().handle_no_permission()


class ProductsByCategoryView(View):
    """Представление для отображения продуктов по категории."""

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = get_product_by_category(category_id)
        context = {
            "products": products,
            "category": category,
        }
        return render(request, "catalog/products_by_category.html", context)
