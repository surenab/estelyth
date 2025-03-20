from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from estelyth_backend.agents.models import Company
from estelyth_backend.agents.models import Seller
from estelyth_backend.agents.models import SellerTypeEnum
from estelyth_backend.locations.api.serializers import AddressSerializer
from estelyth_backend.locations.models import Address

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)  # Allow full address for creation
    company = CompanySerializer(required=False)
    seller_type = serializers.ChoiceField(choices=SellerTypeEnum.choices())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Seller
        fields = "__all__"

    def validate(self, data):
        """Ensure 'user' is required during creation but ignored in updates."""
        if self.instance is None:  # Creation
            if "user" not in data or data["user"] is None:
                raise serializers.ValidationError({"user": "This field is required during creation."})
        return data

    def create(self, validated_data):
        # Handle address creation within an atomic block
        address_data = validated_data.pop("address", None)
        company_data = validated_data.pop("company", None)

        with transaction.atomic():
            if company_data:
                company, _ = Company.objects.get_or_create(**company_data)
                validated_data["company"] = company

            if address_data:
                address = Address.objects.create(**address_data)
                # Set the address to the validated data
                validated_data["address"] = address

            # Create the Seller instance
            return Seller.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Pop the address data from the validated data, if provided
        address_data = validated_data.pop("address", None)
        company_data = validated_data.pop("company", None)

        with transaction.atomic():
            if company_data:
                company, created = Company.objects.get_or_create(**company_data)
                instance.company = company  # Assign the existing or newly created company

            # Check if the seller already has an address
            if address_data:
                # Only process address data if it's not just the country
                if "country" in address_data and not any(
                    key in address_data
                    for key in [
                        "address1",
                        "address2",
                        "address3",
                        "address4",
                        "city",
                        "postal_code",
                        "county",
                        "local_authority",
                    ]
                ):
                    # Ignore the update if only country is provided
                    address_data = None

                if address_data:
                    # If address already exists for the seller, update it
                    if instance.address:
                        # Update each field in the existing address
                        for attr, value in address_data.items():
                            setattr(instance.address, attr, value)
                        instance.address.save()  # Save the updated address

                    else:
                        # Create a new address if the seller doesn't have one
                        address = Address.objects.create(**address_data)
                        instance.address = address  # Assign the newly created address to the seller

            # Update other fields on the Seller model
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            # Save the updated Seller instance
            instance.save()

        return instance
