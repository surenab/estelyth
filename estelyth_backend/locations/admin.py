# locations/admin.py
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Address


@admin.register(Address)
class AddressAdmin(GISModelAdmin):
    list_display = ("address1", "city", "country", "postal_code")
    search_fields = (
        "address1",
        "address2",
        "city",
        "county",
        "postal_code",
        "country",
    )
    list_filter = ("country", "city")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "address1",
                    "address2",
                    "address3",
                    "address4",
                    "city",
                    "county",
                    "postal_code",
                    "local_authority",
                    "country",
                )
            },
        ),
        (
            "Location",
            {
                "fields": ("location",),
                "classes": (
                    "collapse",
                ),  # Collapse the location field by default if desired
            },
        ),
    )
