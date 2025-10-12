from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser


class RegisterView(CreateView):
    """Представление для создания нового пользователя."""

    form_class = MyUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        """Отправка электронного письма с приветствием."""
        subject = "Добро пожаловать в наш магазин!"
        message = "Спасибо за Ваш выбор!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""

    model = MyUser
    form_class = MyUserChangeForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy("catalog:products_list")

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user
