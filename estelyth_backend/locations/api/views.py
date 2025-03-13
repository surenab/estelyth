from django_countries import countries
from rest_framework import viewsets
from rest_framework.response import Response

from estelyth_backend.locations.api.serializers import AddressSerializer
from estelyth_backend.locations.api.serializers import CountrySerializer
from estelyth_backend.locations.models import Address


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CountriesViewSet(viewsets.ViewSet):
    """
    ViewSet for listing countries with flags using django-countries.
    """

    def list(self, request):
        # django_countries.countries is an iterable returning (code, name) pairs.
        data = [{"code": code, "name": name} for code, name in countries]
        serializer = CountrySerializer(data, many=True)
        return Response(serializer.data)
