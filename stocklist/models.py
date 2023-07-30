from django.db import models

# Create your models here.
# Create two models, one for Item and one for Quantity
# Model Item represents individual items
# Model Quantity represents the quantity of each item


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Quantity(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} units of {self.item}"
