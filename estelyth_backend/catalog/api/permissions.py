from rest_framework import permissions


class CategoryPermission(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone,
    but restrict modifications to admin users only.
    """

    def has_permission(self, request, view):
        # Allow read-only methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Restrict modifications to admin users
        return request.user and request.user.is_staff
