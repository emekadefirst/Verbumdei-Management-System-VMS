from django.db import models

class InventoryType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(InventoryType, related_name='type', on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    quantity = models.IntegerField()
    time_of_purchase = models.DateTimeField(auto_now=True)
    