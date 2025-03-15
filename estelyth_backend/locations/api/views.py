from django_countries import countries
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from estelyth_backend.locations.api.permissions import AddressPermission
from estelyth_backend.locations.api.serializers import AddressSerializer
from estelyth_backend.locations.api.serializers import CountrySerializer
from estelyth_backend.locations.models import Address


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AddressPermission]

    def perform_create(self, serializer):
        # Extra safeguard: enforce that only admin users can create addresses.
        if not self.request.user.is_staff:
            msg = "Only admin users can create an address."
            raise PermissionDenied(msg)
        serializer.save()


class CountriesViewSet(viewsets.ViewSet):
    """
    ViewSet for listing countries with flags using django-countries.
    """

    permission_classes = [AddressPermission]

    def list(self, request):
        # django_countries.countries is an iterable returning (code, name) pairs.
        data = [{"code": code, "name": name} for code, name in countries]
        serializer = CountrySerializer(data, many=True)
        return Response(serializer.data)
