from rest_framework import permissions


class IsOwnerReadOnly(permissions.BasePermission):
    """User permission to allow only the company owner to access the GET method.
    For other authorised users, only the PATCH method is available.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return True
        return obj.is_owner(request.user.id)


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow read-only access to any authorized user,
    and full access to the owner of the company.

    This permission class checks if the request user is the owner of the company for
    methods other than methods (GET, HEAD, OPTIONS)
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.is_owner(request.user.id)


class IsCompanyOwner(permissions.BasePermission):
    """Custom permission to allow the company owner to have full access.

    This permission class checks if the request user is the owner of the company.
    """
    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user.id)
