from django.db import models
import uuid

# Create your models here.


class Loans(models.Model):

    """
    Representa un préstamo en la base de datos.

    Atributos:
    - created_at (DateTimeField): La fecha y hora de creación del préstamo.
    - updated_at (DateField): La fecha de la última actualización del préstamo.
    - external_id (UUIDField): El identificador único del préstamo (UUID).
    - amount (DecimalField): La cantidad del préstamo.
    - contract_version (CharField): La versión del contrato del préstamo.
    - status (IntegerField): El estado del préstamo, puede ser 'Pendiente' (1), 'Activo' (2), 'Rechazado' (3) o 'Pagado' (4).
    - outstanding (DecimalField): El saldo pendiente del préstamo.
    - customer (ForeignKey): Una relación con el cliente asociado al préstamo.

    """

    status_options = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    )

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False,
                                   unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    contract_version = models.CharField(max_length=60, default='')
    status = models.IntegerField(choices=status_options, default=2)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey('customers_app.Customer',
                                 on_delete=models.CASCADE,
                                 to_field='external_id',
                                 null=True)
