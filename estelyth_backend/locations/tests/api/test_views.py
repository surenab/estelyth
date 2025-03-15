import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory

from estelyth_backend.locations.api.serializers import AddressSerializer
from estelyth_backend.locations.api.views import AddressViewSet
from estelyth_backend.locations.api.views import CountriesViewSet
from estelyth_backend.locations.models import Address
from estelyth_backend.users.models import User

fake = Faker()


class TestAddressViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_address(self, address: Address, api_rf: APIRequestFactory):
        view = AddressViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/addresses/{address.pk}/"
        request = api_rf.get(url)
        response = view(request, pk=address.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == AddressSerializer(address).data

    def test_create_address_permission_denied(
        self,
        api_rf: APIRequestFactory,
        user: User,
    ):
        # Try to create address as a non-admin user
        view = AddressViewSet.as_view({"post": "create"})
        address_data = {
            "address1": fake.address(),
            "address2": "Suite 500",
            "city": "Test City",
            "postal_code": "12345",
            "country": "US",
        }
        request = api_rf.post("/api/v1/addresses/", data=address_data)
        request.user = user  # non-admin user

        view.request = request

        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_address(self, admin: User, api_rf: APIRequestFactory):
        # Try to create address as an admin user
        view = AddressViewSet.as_view({"post": "create"})
        long = fake.longitude()
        lat = fake.latitude()
        address_data = {
            "address1": fake.address(),
            "address2": "Suite 500",
            "city": "Test City",
            "postal_code": "12345",
            "country": "US",
            "location": f"POINT({long} {lat})",
        }
        request = api_rf.post(
            "/api/v1/addresses/",
            data=address_data,
        )
        request.user = admin

        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert address_data.get("address1") == response.data.get("properties").get("address1")
        assert address_data.get("address2") == response.data.get("properties").get("address2")
        assert address_data.get("city") == response.data.get("properties").get("city")
        assert address_data.get("postal_code") == response.data.get("properties").get("postal_code")
        assert address_data.get("country") == response.data.get("properties").get("country")
        coordinates = response.data.get("geometry").get("coordinates")
        assert float(coordinates[0]) == float(long)
        assert float(coordinates[1]) == float(lat)

    def test_update_address(self, admin: User, address: Address, api_rf: APIRequestFactory):
        # Try to update an address as an admin user
        view = AddressViewSet.as_view({"put": "update"})
        new_address_data = {
            "address1": "Updated Address",
            "address2": "Updated Suite 500",
            "city": "Updated City",
            "postal_code": "67890",
            "country": "US",
            "location": f"POINT({fake.longitude()} {fake.latitude()})",
        }
        url = f"/api/v1/addresses/{address.pk}/"
        request = api_rf.put(url, data=new_address_data)
        request.user = admin

        response = view(request, pk=address.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("properties").get("address1") == new_address_data["address1"]
        assert response.data.get("properties").get("address2") == new_address_data["address2"]
        assert response.data.get("properties").get("city") == new_address_data["city"]
        assert response.data.get("properties").get("postal_code") == new_address_data["postal_code"]
        assert response.data.get("properties").get("country") == new_address_data["country"]

    def test_update_address_permission_denied(self, admin: User, user: User, api_rf: APIRequestFactory):
        # Try to update an address as an admin user
        create_view = AddressViewSet.as_view({"post": "create"})
        long = fake.longitude()
        lat = fake.latitude()
        address_data = {
            "address1": fake.address(),
            "address2": "Suite 500",
            "city": "Test City",
            "postal_code": "12345",
            "country": "US",
            "location": f"POINT({long} {lat})",
        }
        request = api_rf.post(
            "/api/v1/addresses/",
            data=address_data,
        )
        request.user = admin

        response = create_view(request)
        pk = response.data.get("id")

        view = AddressViewSet.as_view({"put": "update"})
        new_address_data = {
            "address1": "Updated Address",
            "address2": "Updated Suite 500",
            "city": "Updated City",
            "postal_code": "67890",
            "country": "US",
            "location": f"POINT({fake.longitude()} {fake.latitude()})",
        }
        url = f"/api/v1/addresses/{pk}/"
        request = api_rf.put(url, data=new_address_data)
        request.user = user

        response = view(request, pk=pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_address(self, admin: User, address: Address, api_rf: APIRequestFactory):
        # Try to delete an address as an admin user
        view = AddressViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/addresses/{address.pk}/"
        request = api_rf.delete(url)
        request.user = admin

        response = view(request, pk=address.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Address.objects.filter(pk=address.pk).count() == 0

    def test_delete_address_permission_denied(self, user: User, address: Address, api_rf: APIRequestFactory):
        # Try to delete an address as an admin user
        view = AddressViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/addresses/{address.pk}/"
        request = api_rf.delete(url)
        request.user = user

        response = view(request, pk=address.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCountriesViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_list_countries(self, api_rf: APIRequestFactory):
        view = CountriesViewSet.as_view({"get": "list"})
        request = api_rf.get("/api/v1/countries/")
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        # Assuming you want to test if countries are returned in the response
        assert len(response.data) > 0
        assert "code" in response.data[0]
        assert "name" in response.data[0]
