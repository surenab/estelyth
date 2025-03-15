from django.urls import resolve
from django.urls import reverse

from estelyth_backend.locations.models import Address


def test_user_detail(address: Address):
    assert reverse("api:address-detail", kwargs={"pk": address.pk}) == f"/api/v1/addresses/{address.pk}/"
    assert resolve(f"/api/v1/addresses/{address.pk}/").view_name == "api:address-detail"


def test_user_list():
    assert reverse("api:address-list") == "/api/v1/addresses/"
    assert resolve("/api/v1/addresses/").view_name == "api:address-list"
