from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Create two models, one for Item and one for Quantity
# Model Item has the quantity of each item.
# Quantity is of type PositiveIntegerField to ensure the quantity value won't be negative



class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0.01)])
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)  # Add reorder_level field to Item model
    status = models.BooleanField(default=True)  # Add status field (True for active, False for inactive)

    # Threshold for reordering the item, must be a positive integer
    reorder_threshold = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name} (Price: €{self.price}, Quantity: {self.quantity})"

    def needs_reorder(self):
        # Determines if the item needs to be reordered based on its current quantity and the associated reorder threshold.
        return self.quantity < self.reorder_threshold

# Each item can have a configurable reorder threshold
class Threshold(models.Model):
    # Use string reference to avoid circular import issues
    item = models.OneToOneField('Item', on_delete=models.CASCADE, related_name='threshold')
    value = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1)])

    def clean(self):
        if self.value < 1:
            raise ValidationError('Reorder threshold must be a positive integer.')

    def __str__(self):
        return f"Threshold for {self.item.name}: {self.value}"

    class Meta:
        verbose_name_plural = "Thresholds"


