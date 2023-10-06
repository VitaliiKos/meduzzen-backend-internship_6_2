from django.contrib import admin

from .models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the UserModel."""

    list_display = ['first_name', 'last_name', 'email']