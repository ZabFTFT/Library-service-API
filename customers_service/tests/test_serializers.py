from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.test import APITestCase

from customers_service.serializers import (
    CustomerCreateSerializer,
    CustomerManageSerializer,
    CustomerChangePasswordSerializer,
    AuthTokenSerializer,
)


class CustomerCreateSerializerTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            "email": "test@test.com",
            "password": "testpass123",
        }
        self.serializer = CustomerCreateSerializer(data=self.valid_payload)

    def test_valid_payload(self):
        self.assertTrue(self.serializer.is_valid())

    def test_create(self):
        user = self.serializer.create(self.valid_payload)
        self.assertEqual(user.email, self.valid_payload["email"])
        self.assertTrue(user.check_password(self.valid_payload["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_password_min_length(self):
        invalid_payload = {"email": "test@test.com", "password": "test"}
        serializer = CustomerCreateSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(
            serializer.errors["password"][0],
            "Ensure this field has at least 5 characters.",
        )


class CustomerManageSerializerTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )
        self.serializer = CustomerManageSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ["id", "email", "first_name", "last_name", "is_staff"]
        )

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["email"], self.user.email)

    def test_first_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["first_name"], self.user.first_name)

    def test_last_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["last_name"], self.user.last_name)

    def test_is_staff_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["is_staff"], self.user.is_staff)

    def test_update_customer_info(self):
        serializer = CustomerManageSerializer(
            instance=self.user,
            data={"first_name": "Jane", "last_name": "Doe"},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Doe")


class AuthTokenSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        self.serializer_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_valid_serializer_data(self):
        serializer = AuthTokenSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["customer"], self.user)

    def test_invalid_email(self):
        serializer_data = {
            "email": "wrong@example.com",
            "password": "testpassword",
        }

        serializer = AuthTokenSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Unable to log in with provided credentials.",
            serializer.errors["non_field_errors"],
        )

    def test_invalid_password(self):
        serializer_data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }

        serializer = AuthTokenSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Unable to log in with provided credentials.",
            serializer.errors["non_field_errors"],
        )

    def test_missing_email(self):
        serializer_data = {
            "password": "testpassword",
        }

        serializer = AuthTokenSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("This field is required.", serializer.errors["email"])

    def test_missing_password(self):
        serializer_data = {
            "email": "test@example.com",
        }

        serializer = AuthTokenSerializer(data=serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("This field is required.", serializer.errors["password"])
