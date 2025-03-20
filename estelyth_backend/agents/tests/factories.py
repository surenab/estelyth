import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker

from estelyth_backend.agents.models import Company
from estelyth_backend.agents.models import Seller
from estelyth_backend.agents.models import SellerTypeEnum
from estelyth_backend.locations.tests.factories import AddressFactory

User = get_user_model()
fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")


class SellerFactory(DjangoModelFactory):
    class Meta:
        model = Seller

    seller_id = factory.Sequence(lambda n: n + 1000)  # Unique seller_id sequence
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    phone = factory.Faker("phone_number")

    company = factory.SubFactory(CompanyFactory)
    address = factory.SubFactory(AddressFactory)

    profile_image_url = factory.Faker("image_url")
    profile_rounded_image_url = factory.Faker("image_url")
    standard_logo_url = factory.Faker("image_url")
    square_logo_url = factory.Faker("image_url")

    background_colour = factory.Faker("hex_color")
    seller_type = factory.Iterator([tag.value for tag in SellerTypeEnum])
    seller_source = factory.Faker("word")

    is_active = factory.Faker("boolean")

    created_at = factory.Faker("date_time_this_decade")
    updated_at = factory.Faker("date_time_this_decade")
