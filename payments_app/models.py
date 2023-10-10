from django.db import models
from loans_app.models import Loans
import uuid

# Create your models here.


class Payments(models.Model):

    status_options = (
        (1, 'Completed'),
        (2, 'Rejected')
    )

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False,
                                   unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.IntegerField(choices=status_options)


class PaymentDetail(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False,
                                   unique=True)
    payment_id = models.ForeignKey(Payments, to_field='external_id',
                                   on_delete=models.CASCADE,
                                   related_name="payment_details")

    loan = models.ForeignKey(Loans, to_field='external_id',
                             on_delete=models.CASCADE,
                             related_name="payment_details")

    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)