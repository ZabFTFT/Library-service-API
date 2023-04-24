from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from book_service.serializers import BookDetailSerializer
from .models import Borrowing, Book
from .serializers import BorrowingListSerializer
from book_service.urls import router

BORROWINGS_URL_LIST = reverse("borrowing_service:borrowing-list")
BORROWINGS_URL_DETAIL = reverse("borrowing_service:borrowing-detail", args=[1])

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
            email='testuser@example.com', password='testpass'
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
            expected_return_date=timezone.now() - timezone.timedelta(days=1)
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()

    def test_actual_return_date_after_borrow_date(self):
        borrowing = Borrowing(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=1),
            actual_return_date=timezone.now() - timezone.timedelta(days=1)
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()

    def test_actual_return_date_after_expected_return_date(self):
        borrowing = Borrowing(
            book=self.book,
            customer=self.customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=1),
            actual_return_date=timezone.now() - timezone.timedelta(days=1)
        )
        with self.assertRaises(IntegrityError):
            borrowing.save()


def borrowing_creating(book, customer):
    return Borrowing.objects.create(
            book=book,
            customer=customer,
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=2),
            actual_return_date=timezone.now() + timezone.timedelta(days=4)
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

        self.customer = get_user_model().objects.create_user(
            email='testuser@example.com', password='testpass'
        )
        self.client = APIClient()
        self.client.force_login(self.customer)

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
                "expected_return_date": timezone.now() + timezone.timedelta(
                    days=2),
            }
        )
        self.client.post(
            BORROWINGS_URL_LIST,
            data={
                "book": self.book.pk,
                "customer": self.customer,
                "borrow_date": timezone.now(),
                "expected_return_date": timezone.now() + timezone.timedelta(
                    days=2),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(book.inventory, self.book.inventory - 2)
