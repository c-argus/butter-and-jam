from django.db import models

# Create your models here.
# Create two models, one for Item and one for Quantity
# Model Item has the quantity of each item.
# Quantity is of type PositiveIntegerField to ensure the quantity value won't be negative


class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)  # Add status field (True for active, False for inactive)

    def __str__(self):
        return f"{self.name} (Price: €{self.price}, Quantity: {self.quantity})"

    def needs_reorder(self):
        reorder_threshold = 5

        # Check if the item's quantity is below the reorder threshold
        if self.quantity < reorder_threshold:
            return True
        else:
            return True
