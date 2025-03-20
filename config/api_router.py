from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from estelyth_backend.agents.api.views import CompanyViewSet
from estelyth_backend.agents.api.views import SellerViewSet
from estelyth_backend.catalog.api.views import CategoryViewSet
from estelyth_backend.locations.api.views import AddressViewSet
from estelyth_backend.locations.api.views import CountriesViewSet
from estelyth_backend.real_estate.api.views import RealEstateViewSet
from estelyth_backend.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("real-estate", RealEstateViewSet, basename="real_estate")
router.register("addresses", AddressViewSet, basename="address")
router.register("countries", CountriesViewSet, basename="country")
router.register("sellers", SellerViewSet, basename="seller")
router.register("companies", CompanyViewSet, basename="company")
router.register("categories", CategoryViewSet, basename="category")

app_name = "api"
urlpatterns = router.urls
