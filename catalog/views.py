from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import ProductForm
from .models import Category, Contact, Product

PER_PAGE = 8


def home(request):
    """Отображает главную страницу."""
    products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "categories": categories}
    return render(request, "catalog/product_list.html", context)


def contacts(request):
    """Работа с контактами."""
    template = "contacts.html"
    contact_details = Contact.objects.all()
    context = {"contacts": contact_details}
    if request.method == "POST":
        user_name = request.POST.get("name")
        phone = request.POST.get("phone")
        user_message = request.POST.get("message")
        filename = f"сообщение_от_{user_name}.txt"
        message = f"Пользователь: {user_name} (телефон: {phone}) оставил сообщение '{user_message}'"
        file = open(filename, "w", encoding="utf-8")
        file.write(message)
        file.close()
        messages.add_message(
            request,
            messages.INFO,
            f"Спасибо, {user_name}! Данные успешно переданы.",
        )
    return render(request, template, context)


def product_detail(request, pk):
    """Отображение детальной информации о продукте."""
    product = Product.objects.get(id=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def product_create(request):
    """Создание нового продукта."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, f"Продукт '{product.name}' успешно создан"
            )
            return redirect("catalog:product_detail", pk=product.id)
    form = ProductForm()
    return render(request, "catalog/product_create.html", {"form": form})
