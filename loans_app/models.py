from django.db import models
import uuid

# Create your models here.


class Customers(models.Model):

    status_options = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    )

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False,
                                   unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    contract_version = models.CharField()
    status = models.IntegerField(choices=status_options)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
