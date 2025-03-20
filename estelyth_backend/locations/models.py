# locations/models.py
from django.contrib.gis.db import models as geomodels
from django.db import models
from django_countries.fields import CountryField


class Address(models.Model):
    address1 = models.CharField(max_length=255, blank=True, default="", db_index=True)
    address2 = models.CharField(max_length=255, blank=True, default="")
    address3 = models.CharField(max_length=255, blank=True, default="")
    address4 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, db_index=True)
    postal_code = models.CharField(max_length=20)
    county = models.CharField(max_length=100, blank=True, default="")
    # Use CountryField from django-countries (powered by pycountry)
    country = CountryField(blank_label="(select country)", db_index=True)
    local_authority = models.CharField(max_length=100, blank=True, default="")
    # GeoDjango PointField for spatial queries (SRID 4326 for WGS84)
    location = geomodels.PointField(
        geography=True,
        blank=True,
        srid=4326,
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["city", "country"]),
            models.Index(fields=["postal_code"]),
            models.Index(fields=["local_authority"]),
            geomodels.Index(fields=["location"]),  # Geospatial index
        ]

    def __str__(self):
        return f"{self.address1 or self.city}, {self.country.name}"
