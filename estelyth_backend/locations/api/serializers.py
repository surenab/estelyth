from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from estelyth_backend.locations.models import Address


class AddressSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Address
        geo_field = "location"
        fields = [
            "id",
            "address1",
            "address2",
            "address3",
            "address4",
            "city",
            "postal_code",
            "county",
            "country",
            "local_authority",
        ]


class CountrySerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    flag = serializers.SerializerMethodField()

    def get_flag(self, obj):
        return f"https://flagcdn.com/w320/{obj['code'].lower()}.png"  # Standard flag URL
