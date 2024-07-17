from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
# Create two models, one for Item and one for Quantity
# Model Item has the quantity of each item.
# Quantity is of type PositiveIntegerField to ensure the quantity value won't be negative


class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0.01)]
    )
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)  # Add reorder_level field to Item model
    status = models.BooleanField(default=True)  # Add status field (True for active, False for inactive)

    # Threshold for reordering the item, must be a positive integer
    reorder_threshold = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name} (Price: €{self.price}, Quantity: {self.quantity})"

    def needs_reorder(self):
        # Method to check if the item needs to be reordered
        return self.quantity < self.reorder_threshold

    class Meta:
        # Meta class to define additional model options

        # Specify default ordering of items by their name in ascending order
        ordering = ['name']

        # Define an index on the name field to improve lookup performance
        indexes = [
            models.Index(fields=['name']),
        ]
