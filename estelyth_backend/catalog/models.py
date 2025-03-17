from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Parent Category",
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
        help_text="Auto-generated from the name if left blank.",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Description",
        help_text="Provide a brief description of the category.",
    )
    icon = models.ImageField(
        upload_to="category_icons/",
        blank=True,
        null=True,
        verbose_name="Category Icon",
        help_text="Optional icon for UI display.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At") 
    """"fndgjkfndgjkfesdbn gsvjkfdnfjkdn vfjklfedn fvjkdaxnv jkfbnfjkdn gvjkfdngjkldn gfvjklrdn gjkl"""

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} (Parent: {self.parent.name if self.parent else 'None'})"

    def save(self, *args, **kwargs):
        """Auto-generate slug before saving"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_full_path(self):
        """Returns the full category path as a string"""
        categories = []
        category = self
        while category:
            categories.append(category.name)
            category = category.parent
        return " > ".join(reversed(categories))
