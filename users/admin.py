from django.contrib import admin

from .models import MyUser


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    pass
