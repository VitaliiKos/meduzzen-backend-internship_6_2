from django.contrib import admin

from .models import CompanyModel


class CompanyModelAdmin(admin.ModelAdmin):
    """Admin configuration for CompanyModel."""

    verbose_name_plural = "Companies"

    search_fields = ('name',)

    list_filter = ('status',)


admin.site.register(CompanyModel, CompanyModelAdmin)
