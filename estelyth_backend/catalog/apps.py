import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogConfig(AppConfig):
    name = "estelyth_backend.catalog"
    verbose_name = _("Catalog")

    def ready(self):
        with contextlib.suppress(ImportError):
            import estelyth_backend.catalog.signals  # noqa: F401
