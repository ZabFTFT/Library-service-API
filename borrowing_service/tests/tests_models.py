from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone

from borrowing_service.models import Borrowing, Book


BORROWINGS_URL_LIST = reverse("borrowing_service:borrowings-list")
BORROWINGS_URL_DETAIL = reverse(
    "borrowing_service:borrowings-detail", args=[1]
)


class BorrowingModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Joane Rowling",
            cover="HARD",
            inventory=10,
            daily_fee=0.50,
        )
        self.customer = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpass"
        )

    def test_borrow_date_before_expected_return_date(self):
        borrowing = Borrowing(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() - timezone.timedelta(days=1),
            actual_return_date=timezone.now(),
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()

    def test_expected_return_date_after_borrow_date(self):
        borrowing = Borrowing(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() - timezone.timedelta(days=1),
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()

    def test_actual_return_date_after_borrow_date(self):
        borrowing = Borrowing(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=1),
            actual_return_date=timezone.now() - timezone.timedelta(days=1),
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()
