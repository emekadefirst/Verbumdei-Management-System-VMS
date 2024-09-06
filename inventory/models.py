from django.db import models

class InventoryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Inventory(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.ForeignKey(InventoryType, related_name='type', on_delete=models.CASCADE)
#     name = models.CharField(max_length=55)
#     quantity = models.IntegerField()
#     time_of_purchase = models.DateTimeField(auto_now=True)


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        InventoryType, related_name="type", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=55)
    quantity = models.IntegerField(null=True, blank=True)
    unit_cost = models.FloatField(null=True, blank=True)
    time_of_purchase = models.DateTimeField(auto_now=True)

    @property
    def total_cost(self):
        if self.quantity is not None and self.unit_cost is not None:
            return self.quantity * self.unit_cost
        return None

    def __str__(self):
        return self.name
