from django.conf import settings
from django.db import models


class Seller(models.Model):
    seller_id = models.IntegerField(unique=True)
    # Optional relation to Django's built-in user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sellers",
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    branch = models.CharField(max_length=255, blank=True)
    # Assume Address is defined in the "locations"
    # app use a string reference if needed.
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    profile_image = models.URLField(max_length=500, blank=True)
    profile_rounded_image = models.URLField(max_length=500, blank=True)
    standard_logo = models.URLField(max_length=500, blank=True)
    square_logo = models.URLField(max_length=500, blank=True)
    background_colour = models.CharField(max_length=50, blank=True)
    seller_type = models.CharField(max_length=50, blank=True)
    available = models.BooleanField(default=True)
    seller_source = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
