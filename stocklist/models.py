from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    reorder_threshold = models.PositiveIntegerField(default=10)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def needs_reorder(self):
        return self.quantity < self.reorder_threshold

    def __str__(self):
        return self.name

class Notification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message





