from django.db import models
from enum import Enum

from borrowing_service.models import Borrowing


class Payment(models.Model):
    class PaymentStatus(models.TextChoices, Enum):
        PENDING = "PENDING"
        PAID = "PAID"

    class PaymentType(models.TextChoices, Enum):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=255,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    type = models.CharField(
        max_length=255,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT,
    )

    class Meta:
        default_related_name = "payments"
