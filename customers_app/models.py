from django.db import models
import uuid


# Create your models here.
class Customer(models.Model):

    status_options = (
        (1, 'Activo'),
        (2, 'Inactivo')
    )

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=status_options) 
