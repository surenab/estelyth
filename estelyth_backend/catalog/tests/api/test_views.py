from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.utils.text import slugify
from faker import Faker
from PIL import Image
from rest_framework import status
from rest_framework.test import APIRequestFactory

from estelyth_backend.catalog.api.serializers import CategorySerializer
from estelyth_backend.catalog.api.views import CategoryViewSet
from estelyth_backend.catalog.models import Category
from estelyth_backend.users.models import User

fake = Faker()


class TestCategoryViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def generate_image(self):
        """Generate a fake image using Pillow and return it as a ContentFile."""
        image = Image.new(
            "RGB",
            (100, 100),
            color=(fake.random_int(0, 255), fake.random_int(0, 255), fake.random_int(0, 255)),
        )
        image_io = BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)
        return ContentFile(image_io.read(), name="fake_image.png")

    def test_get_category(self, category: Category, api_rf: APIRequestFactory):
        view = CategoryViewSet.as_view({"get": "retrieve"})
        url = f"/api/v1/categories/{category.pk}/"
        request = api_rf.get(url)
        response = view(request, pk=category.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == CategorySerializer(category).data

    def test_create_category_permission_denied(
        self,
        api_rf: APIRequestFactory,
        user: User,
    ):
        # Try to create category as a non-admin user
        view = CategoryViewSet.as_view({"post": "create"})
        category_data = {
            "name": fake.name(),
        }
        request = api_rf.post("/api/v1/categories/", data=category_data)
        request.user = user  # non-admin user

        view.request = request

        response = view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category(self, admin: User, api_rf: APIRequestFactory):
        # Try to create category as an admin user
        view = CategoryViewSet.as_view({"post": "create"})
        category_data = {
            "name": fake.name(),
            "description": fake.sentence(),
            "is_active": fake.boolean(),
            "icon": self.generate_image(),
        }
        request = api_rf.post(
            "/api/v1/categories/",
            data=category_data,
        )
        request.user = admin

        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert category_data.get("name") == response.data.get("name")
        assert category_data.get("description") == response.data.get("description")
        assert category_data.get("is_active") == response.data.get("is_active")
        assert type(category_data.get("icon")) is ContentFile
        assert slugify(category_data.get("name")) == response.data.get("slug")

    def test_update_category(self, admin: User, category: Category, api_rf: APIRequestFactory):
        # Try to update an category as an admin user
        view = CategoryViewSet.as_view({"put": "update"})
        new_category_data = {
            "name": fake.name() + "_22",
            "description": fake.sentence() + "_22",
            "is_active": fake.boolean(),
            "icon": self.generate_image(),
        }
        url = f"/api/v1/categories/{category.pk}/"
        request = api_rf.put(url, data=new_category_data)
        request.user = admin

        response = view(request, pk=category.pk)

        assert response.status_code == status.HTTP_200_OK
        assert new_category_data.get("name") == response.data.get("name")
        assert new_category_data.get("description") == response.data.get("description")
        assert new_category_data.get("is_active") == response.data.get("is_active")
        assert type(new_category_data.get("icon")) is ContentFile

    def test_update_category_permission_denied(self, admin: User, user: User, api_rf: APIRequestFactory):
        # Try to update an category as an admin user
        create_view = CategoryViewSet.as_view({"post": "create"})
        category_data = {
            "name": fake.name() + "_22",
            "description": fake.sentence() + "_22",
            "is_active": fake.boolean(),
            "icon": self.generate_image(),
        }
        request = api_rf.post(
            "/api/v1/categories/",
            data=category_data,
        )
        request.user = admin

        response = create_view(request)
        pk = response.data.get("id")

        view = CategoryViewSet.as_view({"put": "update"})
        new_category_data = {
            "name": fake.name() + "_22",
            "description": fake.sentence() + "_22",
            "is_active": fake.boolean(),
        }
        url = f"/api/v1/categories/{pk}/"
        request = api_rf.put(url, data=new_category_data)
        request.user = user

        response = view(request, pk=pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category(self, admin: User, category: Category, api_rf: APIRequestFactory):
        # Try to delete an category as an admin user
        view = CategoryViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/categories/{category.pk}/"
        request = api_rf.delete(url)
        request.user = admin

        response = view(request, pk=category.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.filter(pk=category.pk).count() == 0

    def test_delete_category_permission_denied(self, user: User, category: Category, api_rf: APIRequestFactory):
        # Try to delete an category as an admin user
        view = CategoryViewSet.as_view({"delete": "destroy"})
        url = f"/api/v1/categories/{category.pk}/"
        request = api_rf.delete(url)
        request.user = user

        response = view(request, pk=category.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN
