from rest_framework import permissions


class SellerPermission(permissions.BasePermission):
    """
    Custom permission for Seller:
      - Only authenticated users can access seller-related endpoints.
      - Creation (POST), updating (PUT, PATCH), and deletion (DELETE) are allowed only for admin users.
      - Sellers can update their own seller data but cannot change the 'user' field.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated for all actions.
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow GET, HEAD, OPTIONS for authenticated users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin users can create, update, and delete sellers.
        if request.user.is_staff:
            return True

        # For non-admins, only allow access to update their own seller data.
        return request.method in ["PUT", "PATCH"]

    def has_object_permission(self, request, view, obj):
        # Safe methods are allowed for authenticated users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin users can modify any seller.
        if request.user.is_staff:
            return True

        # Sellers can update their own seller data but not change the 'user' field.
        if request.method in ["PUT", "PATCH"]:
            if "user" in request.data:
                return False  # Prevent modification of 'user' field.
            return obj.user == request.user

        # Non-admin users cannot delete sellers.
        return False
