import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker

from estelyth_backend.catalog.models import Category

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("word")  # Random word as category name
    parent = factory.LazyAttribute(
        lambda o: None if fake.random_int(0, 1) else CategoryFactory(),
    )  # Randomly decide if the category has a parent
    slug = factory.LazyAttribute(
        lambda o: slugify(o.name),
    )  # Automatically generate a slug based on the name
    description = factory.Faker("sentence")  # Random sentence as description
    is_active = factory.Faker("boolean", chance_of_getting_true=100)  # 80% chance of being active
    created_at = factory.Faker("date_this_year")  # Random date this year
    updated_at = factory.Faker("date_this_month")  # Random date this month

    class Meta:
        model = Category
