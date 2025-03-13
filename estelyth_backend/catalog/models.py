from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        return f"{self.name} (Parent: {self.parent.name if self.parent else 'None'})"
