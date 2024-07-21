from uuid import uuid4
from django.core.validators import MinValueValidator
from django.db import models

from baby_sitting.models import Baby


# Create your models here.
class StoreEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_cost = models.IntegerField(validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_entries"


class BoughtItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    baby = models.ForeignKey(Baby, models.DO_NOTHING, related_name="bought_items")
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.IntegerField(validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bought_items"
