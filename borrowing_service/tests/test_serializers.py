from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from borrowing_service.models import Borrowing, Book
from borrowing_service.serializers import BorrowingCreateSerializer

BORROWINGS_URL_LIST = reverse("borrowing_service:borrowings-list")
BORROWINGS_URL_DETAIL = reverse(
    "borrowing_service:borrowings-detail", args=[1]
)


def borrowing_creating(book, customer):
    return Borrowing.objects.create(
        book=book,
        customer=customer,
        borrow_date=timezone.now(),
        expected_return_date=timezone.now() + timezone.timedelta(days=2),
        actual_return_date=timezone.now() + timezone.timedelta(days=4),
    )


class BorrowingSerializerTest(TestCase):
    def setUp(self) -> None:
        self.book = Book.objects.create(
            title="Test Book",
            author="Joane Rowling",
            cover="HARD",
            inventory=10,
            daily_fee=0.50,
        )

        self.customer = get_user_model().objects.create_superuser(
            email="testuser@example.com", password="testpass"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.customer)

    def test_list_borrowings(self):
        borrowing_creating(self.book, self.customer)
        borrowing_creating(self.book, self.customer)
        borrowing_creating(self.book, self.customer)

        response = self.client.get(BORROWINGS_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_detail_borrowing(self):
        borrowing_creating(self.book, self.customer)
        response = self.client.get(BORROWINGS_URL_DETAIL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_borrowing_decrease_book_inventory(self):
        response = self.client.post(
            BORROWINGS_URL_LIST,
            data={
                "book": self.book.pk,
                "customer": self.customer,
                "borrow_date": timezone.now(),
                "expected_return_date": timezone.now()
                + timezone.timedelta(days=2),
            },
        )
        self.client.post(
            BORROWINGS_URL_LIST,
            data={
                "book": self.book.pk,
                "customer": self.customer.pk,
                "borrow_date": timezone.now(),
                "expected_return_date": timezone.now()
                + timezone.timedelta(days=2),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(book.inventory, self.book.inventory - 2)

    def test_cant_create_borrowing_if_inventory_zero(self):
        book = Book.objects.create(
            title="Test Book",
            author="Joane Rowling",
            cover="HARD",
            inventory=0,
            daily_fee=0.50,
        )

        borrowing_data = {
            "borrow_date": "2023-04-24",
            "expected_return_date": "2023-05-01",
            "actual_return_date": None,
            "book": book.id,
        }
        serializer = BorrowingCreateSerializer(data=borrowing_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
