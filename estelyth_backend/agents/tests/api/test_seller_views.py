import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory

from estelyth_backend.agents.api.views import SellerViewSet
from estelyth_backend.agents.models import Seller
from estelyth_backend.users.models import User

fake = Faker()


class TestSellerViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_seller(self, admin: User, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.get(url)
        request.user = admin
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_get_seller_owner(self, user: User, seller: Seller, api_rf: APIRequestFactory):
        seller.user = user
        seller.save()

        view = SellerViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.get(url)
        request.user = user
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_get_seller_forbidden(self, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.get(url)
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_seller_permission_denied(self, api_rf: APIRequestFactory, user: User):
        view = SellerViewSet.as_view({"post": "create"})
        seller_data = {"name": "Test Seller", "seller_id": 12345}
        request = api_rf.post("/api/v1/sellers/", data=seller_data)
        request.user = user
        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_seller_basic(self, admin: User, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"post": "create"})
        seller_data = {
            "name": "Test Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
            "user": admin.pk,
        }
        request = api_rf.post("/api/v1/sellers/", data=seller_data)
        request.user = admin
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("address") is None
        assert response.data.get("company") is None
        assert response.data.get("seller_type") == seller_data.get("seller_type")
        assert response.data.get("seller_id") == seller_data.get("seller_id")
        assert response.data.get("user") == seller_data.get("user")
        assert response.data.get("name") == seller_data.get("name")

    def test_create_seller_with_address(self, admin: User, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"post": "create"})
        seller_data = {
            "name": "Test Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
            "user": admin.pk,
            "address": {
                "address1": fake.address(),
                "address2": "Suite 500",
                "city": "Test City",
                "postal_code": "12345",
                "country": "US",
            },
        }
        request = api_rf.post("/api/v1/sellers/", data=seller_data, format="json")
        request.user = admin
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        address_data = seller_data.get("address")
        assert address_data.get("address1") == response.data.get("address").get("properties").get("address1")
        assert address_data.get("address2") == response.data.get("address").get("properties").get("address2")
        assert address_data.get("city") == response.data.get("address").get("properties").get("city")
        assert address_data.get("postal_code") == response.data.get("address").get("properties").get("postal_code")
        assert address_data.get("country") == response.data.get("address").get("properties").get("country")
        assert response.data.get("company") is None
        assert response.data.get("seller_type") == seller_data.get("seller_type")
        assert response.data.get("seller_id") == seller_data.get("seller_id")
        assert response.data.get("user") == seller_data.get("user")
        assert response.data.get("name") == seller_data.get("name")

    def test_create_seller_with_address_company(self, admin: User, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"post": "create"})
        seller_data = {
            "name": "Test Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
            "user": admin.pk,
            "address": {
                "address1": fake.address(),
                "address2": "Suite 500",
                "city": "Test City",
                "postal_code": "12345",
                "country": "US",
            },
            "company": {
                "name": "Test Comapny",
            },
        }
        request = api_rf.post("/api/v1/sellers/", data=seller_data, format="json")
        request.user = admin
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        address_data = seller_data.get("address")
        assert seller_data.get("company").get("name") == response.data.get("company").get("name")
        assert address_data.get("address1") == response.data.get("address").get("properties").get("address1")
        assert address_data.get("address2") == response.data.get("address").get("properties").get("address2")
        assert address_data.get("city") == response.data.get("address").get("properties").get("city")
        assert address_data.get("postal_code") == response.data.get("address").get("properties").get("postal_code")
        assert address_data.get("country") == response.data.get("address").get("properties").get("country")
        assert response.data.get("seller_type") == seller_data.get("seller_type")
        assert response.data.get("seller_id") == seller_data.get("seller_id")
        assert response.data.get("user") == seller_data.get("user")
        assert response.data.get("name") == seller_data.get("name")

    def test_update_seller(self, admin: User, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"put": "update"})
        updated_data = {
            "name": "Updated Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
        }
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = admin
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == updated_data["name"]

    def test_update_seller_owner(self, user: User, seller: Seller, api_rf: APIRequestFactory):
        seller.user = user
        seller.save()

        view = SellerViewSet.as_view({"put": "update"})
        updated_data = {
            "name": "Updated Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
        }
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = user
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == updated_data["name"]

    def test_update_seller_permission_denied(self, another_user: User, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"put": "update"})
        updated_data = {
            "name": "Updated Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
        }
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = another_user
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_seller_cannot_change_user(
        self,
        user: User,
        seller: Seller,
        another_user: User,
        api_rf: APIRequestFactory,
    ):
        seller.user = user
        seller.save()

        view = SellerViewSet.as_view({"put": "update"})
        updated_data = {
            "user": another_user.pk,
            "name": "Updated Seller",
            "seller_id": 12345,
            "seller_type": "UNKNOWN",
        }
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.put(url, data=updated_data)
        request.user = user
        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_seller(self, admin: User, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.delete(url)
        request.user = admin

        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Seller.objects.filter(pk=seller.pk).count() == 0

    def test_delete_seller_permission_denied(self, user: User, seller: Seller, api_rf: APIRequestFactory):
        view = SellerViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/sellers/{seller.pk}/"
        request = api_rf.delete(url)
        request.user = user

        response = view(request, pk=seller.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN
