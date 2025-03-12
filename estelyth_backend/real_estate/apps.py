import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "estelyth_backend.real_estate"
    verbose_name = _("Real Estate")

    def ready(self):
        with contextlib.suppress(ImportError):
            import estelyth_backend.real_estate.signals  # noqa: F401
