from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

from estelyth_backend.locations.models import Address

User = get_user_model()


class SellerTypeEnum(str, Enum):
    BRANDED_AGENT = "BRANDED_AGENT"
    PRIVATE_USER = "PRIVATE_USER"
    UNBRANDED_AGENT = "UNBRANDED_AGENT"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace("_", " ").title()) for tag in cls]


class Company(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the company")

    def __str__(self):
        return f"Company: {self.name}"


class Seller(models.Model):
    seller_id = models.PositiveIntegerField(unique=True, help_text="Scraped seller ID from daft.ie")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller",
        help_text="The user associated with this seller",
    )

    name = models.CharField(max_length=255, help_text="Seller's full name or business name")
    phone = models.CharField(max_length=50, blank=True, help_text="Contact phone number")

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Company to which this seller belongs",
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Address associated with the seller",
    )

    # Using URL fields instead of ImageField
    profile_image_url = models.URLField(max_length=500, blank=True, help_text="URL of the profile image")
    profile_rounded_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="URL of the rounded profile image",
    )
    standard_logo_url = models.URLField(max_length=500, blank=True, help_text="URL of the standard logo")
    square_logo_url = models.URLField(max_length=500, blank=True, help_text="URL of the square logo")

    background_colour = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI branding")

    seller_type = models.CharField(
        max_length=20,
        choices=SellerTypeEnum.choices(),
        default=SellerTypeEnum.UNKNOWN.value,
        help_text="Type of seller",
    )

    seller_source = models.CharField(max_length=50, blank=True, help_text="Source of the seller (e.g., 'daft.ie')")

    is_active = models.BooleanField(default=True, help_text="Indicates if the seller is active")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp")

    def __str__(self):
        return f"{self.name} ({self.seller_type})"
