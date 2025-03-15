import factory
from django.contrib.gis.geos import Point
from django_countries import countries
from factory.django import DjangoModelFactory
from faker import Faker

from estelyth_backend.locations.models import Address

fake = Faker()


class AddressFactory(DjangoModelFactory):
    address1 = factory.Faker("address")
    address2 = factory.Faker("address")
    address3 = factory.Faker("address")
    address4 = factory.Faker("address")
    city = factory.Faker("city")
    postal_code = factory.Faker("postcode")
    county = factory.Faker("city")
    # Generate a 2-letter country code from django_countries' countries
    country = factory.Iterator([code for code, _ in countries])

    local_authority = factory.Faker("city")
    location = factory.LazyFunction(
        lambda: Point(
            (
                fake.longitude(),
                fake.latitude(),
            ),
        ),
    )

    class Meta:
        model = Address
