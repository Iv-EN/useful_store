from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView

from .forms import ProductForm
from .models import Category, Contact, Product

PRODUCT_PER_PAGE = 8
"""Количество продуктов отображаемых на странице."""


class ProductListView(ListView):
    """
    Представление для отображения списка продуктов с постраничной навигацией.
    """

    model = Product
    paginate_by = PRODUCT_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ContactView(ListView):
    """
    Представление для отображения списка контактов
    с формой для отправки сообщений.
    """

    model = Contact
    template_name = "catalog/contacts.html"

    def post(self, request):
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


class ProductDetailView(DetailView):
    """Представление для отображения детальной информации о продукте."""

    model = Product


class ProductCreateView(CreateView):
    """Представление для создания нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return redirect("catalog:product_detail", pk=product.pk)
