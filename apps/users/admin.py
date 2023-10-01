from django.contrib import admin

from .models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']