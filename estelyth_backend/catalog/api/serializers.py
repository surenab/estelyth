from rest_framework import serializers

from estelyth_backend.catalog.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Includes parent category details (nested) and a full category path.
    """

    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon", "is_active", "parent", "full_path"]
        read_only_fields = ["id", "slug", "full_path"]

    def get_full_path(self, obj):
        """
        Generates the full category path (e.g., "Real Estate > Apartments > Luxury").
        """
        return obj.get_full_path()
