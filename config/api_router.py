from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from estelyth_backend.real_estate.api.views import RealEstateViewSet
from estelyth_backend.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("real-estate", RealEstateViewSet, basename="real_estate")


app_name = "api"
urlpatterns = router.urls
