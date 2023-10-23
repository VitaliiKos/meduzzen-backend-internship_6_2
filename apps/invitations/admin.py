from django.contrib import admin

from .models import InviteModel, RequestModel


class InviteModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Invites"
    list_display = ('user', 'company', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'company')
    search_fields = ('user__email', 'company__name')
    list_per_page = 20


class RequestModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Requests"
    list_display = ('user', 'company', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'company')
    search_fields = ('user__email', 'company__name')
    list_per_page = 20


admin.site.register(InviteModel, InviteModelAdmin)
admin.site.register(RequestModel, RequestModelAdmin)
