from django.test import TestCase
from django.contrib.auth import get_user_model
from customers_service.models import Customer


class CustomerModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )

    def test_check_created_customer(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("testpass123"))
        self.assertEqual(admin_user.first_name, "Admin")
        self.assertEqual(admin_user.last_name, "User")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="testpass123",
                first_name="John",
                last_name="Doe",
            )
