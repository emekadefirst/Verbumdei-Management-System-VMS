from datetime import datetime
from django.db import models
from inventory.models import InventoryType, Inventory


def voucher_code():
    now = datetime.now()
    time_str = now.strftime("%M%S")
    return f"VOCH{time_str}"


class Voucher(models.Model):
    class STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"

    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(InventoryType, related_name="voucher_type", on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    quantity = models.IntegerField(null=True, blank=True)
    unit_cost = models.FloatField(null=True, blank=True)
    code = models.CharField(max_length=20, default=voucher_code)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Save the Voucher. If status changes to APPROVED, move it to the Inventory model.
        """
        super().save(*args, **kwargs)

        if self.status == self.STATUS.APPROVED and self.quantity and self.unit_cost:
            Inventory.objects.get_or_create(
                type=self.type,
                name=self.name,
                quantity=self.quantity,
                unit_cost=self.unit_cost,
            )

    def __str__(self):
        return f"Voucher {self.id} - {self.name} ({self.status})"
