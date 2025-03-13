import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    name = "estelyth_backend.locations"
    verbose_name = _("Locations")

    def ready(self):
        with contextlib.suppress(ImportError):
            import estelyth_backend.locations.signals  # noqa: F401
