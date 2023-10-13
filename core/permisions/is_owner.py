from rest_framework import permissions

from core.enums.user_enum import UserEnum


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.members.filter(pk=request.user.pk, employeemodel__role=UserEnum.OWNER).exists()
