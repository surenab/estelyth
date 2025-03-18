from django.contrib import admin
from django.utils.text import slugify

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}  # Auto-generate slug from the name
    ordering = ("name",)

    # Display subcategories directly on the category page
    inlines = []  # You can add inlines here if you want to add additional related models

    def save_model(self, request, obj, form, change):
        """Ensure slug is auto-generated if not set."""
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
