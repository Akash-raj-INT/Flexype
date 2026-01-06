from django.db import models
import uuid
from django.utils import timezone

class Inventory(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    total_stock = models.IntegerField()

    def __str__(self):
        return self.sku

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expires_at