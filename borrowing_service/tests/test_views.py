from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from borrowing_service.models import Borrowing, Book


BORROWINGS_URL_LIST = reverse("borrowing_service:borrowings-list")
BORROWINGS_URL_DETAIL = reverse(
    "borrowing_service:borrowings-detail", args=[1]
)


class BorrowingViewsTests(TestCase):
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
        self.client = APIClient()
        self.client.force_authenticate(self.customer)

    def test_list_borrowings(self):
        borrowing_1 = Borrowing.objects.create(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now() - timezone.timedelta(days=5),
            expected_return_date=timezone.now() + timezone.timedelta(days=5),
        )
        borrowing_2 = Borrowing.objects.create(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now() - timezone.timedelta(days=10),
            expected_return_date=timezone.now() + timezone.timedelta(days=5),
        )
        response = self.client.get(BORROWINGS_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], borrowing_1.id)

    def test_detail_borrowing(self):
        borrowing = Borrowing.objects.create(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now() - timezone.timedelta(days=5),
            expected_return_date=timezone.now() + timezone.timedelta(days=5),
        )
        response = self.client.get(
            reverse("borrowing_service:borrowings-detail", args=[borrowing.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], borrowing.id)

    def test_create_borrowing_decrease_book_inventory(self):
        response = self.client.post(
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
        self.assertEqual(book.inventory, self.book.inventory - 1)
