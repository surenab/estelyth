import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory

from estelyth_backend.agents.api.views import CompanyViewSet
from estelyth_backend.agents.models import Company
from estelyth_backend.users.models import User

fake = Faker()


class TestCompanyViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_company(self, admin: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.get(url)
        request.user = admin
        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_get_company_forbidden(self, user: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.get(url)
        request.user = user
        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_company_permission_denied(self, api_rf: APIRequestFactory, user: User):
        view = CompanyViewSet.as_view({"post": "create"})
        company_data = {
            "name": fake.company(),
        }
        request = api_rf.post("/api/v1/companies/", data=company_data)
        request.user = user  # non-admin user
        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_company(self, admin: User, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"post": "create"})
        company_data = {
            "name": fake.company(),
        }
        request = api_rf.post("/api/v1/companies/", data=company_data)
        request.user = admin
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED

    def test_update_company(self, admin: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"put": "update"})
        updated_data = {"name": "Updated Company"}
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = admin

        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == updated_data["name"]

    def test_update_company_permission_denied(self, user: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"put": "update"})
        updated_data = {"name": "Updated Company"}
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = user

        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_company(self, admin: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.delete(url)
        request.user = admin

        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Company.objects.filter(pk=company.pk).count() == 0

    def test_delete_company_permission_denied(self, user: User, company: Company, api_rf: APIRequestFactory):
        view = CompanyViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/companies/{company.pk}/"
        request = api_rf.delete(url)
        request.user = user

        response = view(request, pk=company.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN
