from django.contrib import messages
from django.shortcuts import render, redirect


def home(request):
    """Отображает главную страницу."""
    return render(request, "home.html")


def contacts(request):
    """Работа с контактами."""
    template = "contacts.html"
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
            request, messages.INFO, f"Спасибо, {user_name}! Данные успешно переданы."
        )
    return render(request, template)
