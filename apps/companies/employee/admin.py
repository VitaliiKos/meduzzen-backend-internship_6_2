from django.contrib import admin

from .models import EmployeeModel


class EmployeeModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Employee"
    list_display = ('user', 'company', 'role', 'invite_status', 'request_status', 'created_at', 'updated_at')
    list_filter = ('role', 'company', 'invite_status__status', 'request_status__status')
    search_fields = ('user__email', 'company__name')
    list_per_page = 20


admin.site.register(EmployeeModel, EmployeeModelAdmin)
