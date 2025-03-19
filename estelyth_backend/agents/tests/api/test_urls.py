from django.urls import resolve
from django.urls import reverse

from estelyth_backend.agents.models import Company
from estelyth_backend.agents.models import Seller


def test_seller_detail(seller: Seller):
    assert reverse("api:seller-detail", kwargs={"pk": seller.pk}) == f"/api/v1/sellers/{seller.pk}/"
    assert resolve(f"/api/v1/sellers/{seller.pk}/").view_name == "api:seller-detail"


def test_seller_list():
    assert reverse("api:seller-list") == "/api/v1/sellers/"
    assert resolve("/api/v1/sellers/").view_name == "api:seller-list"


def test_company_detail(company: Company):
    assert reverse("api:company-detail", kwargs={"pk": company.pk}) == f"/api/v1/companies/{company.pk}/"
    assert resolve(f"/api/v1/companies/{company.pk}/").view_name == "api:company-detail"


def test_company_list():
    assert reverse("api:company-list") == "/api/v1/companies/"
    assert resolve("/api/v1/companies/").view_name == "api:company-list"
