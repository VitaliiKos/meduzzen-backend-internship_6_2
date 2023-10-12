from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.members.filter(pk=request.user.pk).exists()
