from rest_framework import permissions


class IsCompanyInviteOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.is_owner(request.user)
