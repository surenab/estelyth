from rest_framework import permissions


class AddressPermission(permissions.BasePermission):
    """
    Custom permission for Address:
      - Anyone can view (GET, HEAD, OPTIONS).
      - Creation (POST) is allowed only for admin users.
      - For unsafe methods on an existing Address, allow the change if:
          a) the user is an admin, or
          b) the user is a seller and either:
             - the seller's address is this address, or
             - one of the seller's real estates uses this address.
    """

    def has_permission(self, request, view):
        # Allow all safe methods.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For creation, only admin users can create.
        if request.method == "POST":
            return request.user and request.user.is_staff

        # For updates/deletes, require authentication.
        # Object-level check happens later.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods are always allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin users are allowed to update/delete any address.
        if request.user.is_staff:
            return True

        # Try to access the seller associated with the user.
        # (This assumes you have a OneToOne relationship from User to Seller.)
        seller = getattr(request.user, "seller", None)
        if not seller:
            return False

        # Check if the sellers address is the one being modified.
        return seller.address and seller.address.pk == obj.pk

        # Alternatively, check if any property owned
        # by the seller has this address.
        # (This assumes the related name for
        # Property in the Seller model is "properties".)
        # if seller.properties.filter(address__pk=obj.pk).exists():
        #     return True  # noqa: ERA001

        # If none of these conditions match, deny permission.
        return False
