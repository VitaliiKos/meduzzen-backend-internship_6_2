from rest_framework import permissions

from core.enums.user_enum import UserEnum


class IsCompanyOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.members.filter(pk=request.user.pk, employeemodel__role=UserEnum.OWNER).exists()
