from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class OrderCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

    def test_create_order(self):
        url = reverse("create-order")
        order_data = {
            "user_id": 1,
            "username": "testuser",
            "recipient_name": "John Doe",
            "recipient_tel": "010-1234-5678",
            "address": "123 Test Street",
            "address_detail": "Apt 101",
            "zip_code": "12345",
            "order_request": "12345",
        }
        response = self.client.post(url, order_data, format="json")
        self.assertEqual(response.status_code, 201)
