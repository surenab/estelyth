from django.urls import resolve
from django.urls import reverse

from estelyth_backend.catalog.models import Category


def test_user_detail(category: Category):
    assert reverse("api:category-detail", kwargs={"pk": category.pk}) == f"/api/v1/categories/{category.pk}/"
    assert resolve(f"/api/v1/categories/{category.pk}/").view_name == "api:category-detail"


def test_user_list():
    assert reverse("api:category-list") == "/api/v1/categories/"
    assert resolve("/api/v1/categories/").view_name == "api:category-list"
