from rest_framework import filters
from rest_framework import viewsets

from estelyth_backend.catalog.api.permissions import CategoryPermission
from estelyth_backend.catalog.api.serializers import CategorySerializer
from estelyth_backend.catalog.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing property categories.
    Provides standard CRUD operations with pagination.
    Only active categories are listed for non-admin users.
    """

    queryset = Category.objects.filter(is_active=True)  # Exclude inactive categories
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]  # Only admins can manage categories
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["name", "created_at"]
    search_fields = ["name", "description"]

    def get_queryset(self):
        """
        Admins see all categories, while regular users see only active ones.
        """
        if self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(is_active=True)
