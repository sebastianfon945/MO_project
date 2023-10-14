from django.db import models
import uuid


# Create your models here.
class Customer(models.Model):

    """
    Representa un cliente en la base de datos.

    Atributos:
    - created_at (DateTimeField): La fecha y hora de creación del cliente.
    - updated_at (DateField): La fecha de la última actualización del cliente.
    - external_id (UUIDField): El identificador único del cliente (UUID).
    - score (DecimalField): El puntaje del cliente.
    - status (IntegerField): El estado del cliente, puede ser 'Activo' (1) o 'Inactivo' (2).

    """

    status_options = (
        (1, 'Activo'),
        (2, 'Inactivo')
    )

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=status_options)
