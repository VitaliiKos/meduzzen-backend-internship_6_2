from django.contrib import admin

from apps.invitations.models import EmployeeModel


class EmployeeModelAdmin(admin.ModelAdmin):
    """Admin configuration for Invitations."""

    verbose_name_plural = "Invitations"
    list_display = ('user', 'company', 'invitation_status', 'request_status', 'role')
    search_fields = ('user__username', 'company__name')
    list_filter = ('invitation_status', 'request_status', 'role')


admin.site.register(EmployeeModel, EmployeeModelAdmin)
