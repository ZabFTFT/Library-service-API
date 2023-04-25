from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q
from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = "borrowings"
        constraints = [
            CheckConstraint(
                check=Q(borrow_date__lte=models.F("expected_return_date")),
                name="borrow_date_before_expected_return_date",
            ),
            CheckConstraint(
                check=Q(expected_return_date__gte=models.F("borrow_date")),
                name="expected_return_date_after_borrow_date",
            ),
            CheckConstraint(
                check=Q(actual_return_date__isnull=True)
                | Q(actual_return_date__gte=models.F("borrow_date")),
                name="actual_return_date_after_borrow_date",
            ),
        ]
