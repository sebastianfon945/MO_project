
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Loans
from customers_app.models import Customer


class LoansTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_loan(self):
        customer = Customer.objects.create(
            external_id="2c1d845d-ff3b-4b9e-8c1d-74e97261f7b0", status=1, score=1000
        )
        data = {
            "customer": "test_customer",
            "amount": 500,
            "status": 1,
            "outstanding": 500,
        }
        response = self.client.post("/api/create_loan/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Loans.objects.count(), 1)
        loan = Loans.objects.get()
        self.assertEqual(loan.customer, customer)
        self.assertEqual(loan.amount, data["amount"])
        self.assertEqual(loan.status, data["status"])
        self.assertEqual(loan.outstanding, data["outstanding"])

    def test_list_loans(self):
        response = self.client.get("/api/list_loans/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Loans.objects.count())

    def test_loan_by_id(self):
        customer = Customer.objects.create(
            external_id="1c1d845d-ff3b-4b9e-8c1d-74e97261f7b0", status=1, score=1000
        )
        loan = Loans.objects.create(
            customer=customer, amount=500, status=1, outstanding=500
        )
        response = self.client.get(f"/api/loan_by_id/?external_id={loan.external_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"], customer.external_id)
        self.assertEqual(response.data["amount"], loan.amount)

    def test_loans_by_customer(self):
        customer = Customer.objects.create(
            external_id="2c1d845d-ff3b-4b9e-8c1d-34e97261f7b0", status=1, score=1000
        )
        Loans.objects.create(
            customer=customer, amount=500, status=1, outstanding=500
        )
        response = self.client.get(f"/api/loans_by_customer/?customer=test_customer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Loans.objects.filter(customer=customer).count())