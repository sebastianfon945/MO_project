import json
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Customer
from loans_app.models import Loans


class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        data = {
            "external_id": "2c1d845d-ff3b-4b9e-8c1d-74e97261f7b",
            "status": 1,
            "score": 1000,
        }
        response = self.client.post("/api/create_customer/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.get()
        self.assertEqual(customer.external_id, data["external_id"])
        self.assertEqual(customer.status, data["status"])
        self.assertEqual(customer.score, data["score"])

    def test_list_customer(self):
        Customer.objects.create(
            external_id="2c1d845d-ff3b-4b9e-8c1d-74e97261f7b0", status=1, score=1000
        )
        Customer.objects.create(
            external_id="2c1d845d-ff3b-4b9e-8c1d-74e97261f7b1", status=2, score=500
        )
        response = self.client.get("/api/list_customer/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Customer.objects.count())

    def test_get_balance(self):
        customer = Customer.objects.create(
            external_id="2c1d845d-ff3b-4b9e-8c1d-74e97261f7b2", status=1, score=1000
        )
        Loans.objects.create(
            customer=customer, amount=500, status=2, outstanding=500
        )
        response = self.client.get(f"/api/get_balance/?customer=test_customer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_debt"], 500)
        self.assertEqual(response.data["available_amount"], 500)

        # Test with a customer that doesn't exist
        response = self.client.get("/api/get_balance/?customer=nonexistent_customer")
        self.assertEqual(response.status_code, 400)

        # Test without 'customer' parameter
        response = self.client.get("/api/get_balance/")
        self.assertEqual(response.status_code, 400)