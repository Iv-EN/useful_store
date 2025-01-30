from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView

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


class ProductView(View):
    """Представление для создания и редактирования продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get(self, request, pk=None):
        if pk:
            product = self.model.objects.get(pk=pk)
            form = self.form_class(instance=product)
            title = "Редактировать продукт"
        else:
            form = self.form_class()
            title = "Создать продукт"
        return render(
            request,
            self.template_name,
            {'form': form, 'title': title}
        )

    def post(self, request, pk=None):
        if pk:
            product = self.model.objects.get(pk=pk)
            form = self.form_class(
                request.POST, request.FILES, instance=product
            )
        else:
            form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Продукт успешно создан.")
            return redirect("catalog:product_detail", pk=product.pk)
        title = "Редактировать продукт" if pk else "Создать продукт"
        return render(
            request,
            self.template_name,
            {'form': form, 'title': title}
        )


class ProductDeleteView(DeleteView):
    """Представление для удаления продукта."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удален.")
        return super().delete(request, *args, **kwargs)
