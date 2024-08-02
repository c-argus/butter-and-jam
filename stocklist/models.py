from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
# Create two models, one for Item and one for Quantity
# Model Item has the quantity of each item.
# Quantity is of type PositiveIntegerField to ensure the quantity value won't be negative

class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    # description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0.01)])
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)  # Add reorder_level field to Item model
    status = models.BooleanField(default=True)  # Add status field (True for active, False for inactive)
    reorder_threshold = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1)])
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Price: €{self.price:.2f}, Quantity: {self.quantity})"

    def needs_reorder(self):
        # Determines if the item needs to be reordered based on its current quantity and the associated reorder threshold.
        return self.quantity < self.reorder_threshold

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.needs_reorder() and not Notification.objects.filter(item=self, read=False).exists():
            Notification.objects.create(
                item=self,
                message=f"The stock for {self.name} has fallen below the reorder threshold of {self.reorder_threshold}."
            )

class Notification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # ForeignKey to link the notification to a specific item. When the item is deleted, the notification is also deleted.
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # DateTime field to store when the notification was created. Automatically set to the current date and time when the notification is created.
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.item.name}: {self.message}"









