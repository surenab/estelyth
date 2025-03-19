from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from estelyth_backend.agents.api.permissions import SellerPermission
from estelyth_backend.agents.api.serializers import CompanySerializer
from estelyth_backend.agents.api.serializers import SellerSerializer
from estelyth_backend.agents.models import Company
from estelyth_backend.agents.models import Seller


class SellerPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50  # Limit the max page size for performance


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    permission_classes = [IsAdminUser]


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [SellerPermission]
    pagination_class = SellerPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["user", "name", "address", "seller_type", "is_active"]
    search_fields = ["user", "name", "address", "seller_type", "is_active", "phone"]
