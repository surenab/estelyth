import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AgentsConfig(AppConfig):
    name = "estelyth_backend.agents"
    verbose_name = _("Agents")

    def ready(self):
        with contextlib.suppress(ImportError):
            import estelyth_backend.agents.signals  # noqa: F401
