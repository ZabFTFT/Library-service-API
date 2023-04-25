from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


CREATE_CUSTOMER_URL = reverse("customers_service:register")
MANAGE_CUSTOMER_URL = reverse("customers_service:manage-customer")
CHANGE_PASSWORD_URL = reverse("customers_service:manage-password")
CREATE_TOKEN_URL = reverse("customers_service:token_obtain_pair")


class CustomerTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass123"
        )

    def test_create_customer(self):
        payload = {
            "email": "newcustomer@test.com",
            "password": "testpass123",
            "name": "New Customer",
        }
        response = self.client.post(CREATE_CUSTOMER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payload["email"])
        self.assertFalse("password" in response.data)

    def test_change_customer_info(self):
        self.client.force_authenticate(user=self.user)

        user_data = {"first_name": "Hatake", "last_name": "Kakashi"}

        response = self.client.patch(MANAGE_CUSTOMER_URL, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, user_data["first_name"])
        self.assertEqual(self.user.last_name, user_data["last_name"])

    def test_change_customer_password(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "old_password": "testpass123",
            "password": "newpass123",
            "password2": "newpass123",
        }
        response = self.client.patch(CHANGE_PASSWORD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_create_token(self):
        payload = {"email": self.user.email, "password": "testpass123"}
        response = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in response.data)
        self.assertTrue("access" in response.data)
