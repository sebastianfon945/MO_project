
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from loans_app.models import Loans
from django.db.models import Sum
from .serializer import PaymentsSerializer, PaymentDetailSerializer
from decimal import Decimal


@api_view(['POST'])
def register_payment(request):
    """
    Registra un pago para un cliente en deuda.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene los datos del pago.

    Retorna:
    Response: Un objeto Response que contiene el resultado del registro del pago.

    """
    customer = request.data.get('customer')
    amount = request.data.get('amount')
    request_data = request.data
    payment_details = request.data.get('payment_details')

    loans = Loans.objects.filter(customer=customer, status=2)
    if not loans:
        return Response({"error": "El cliente no tiene deudas activas."},
                        status=status.HTTP_400_BAD_REQUEST)
    total_debt = loans \
        .aggregate(sum_outstanding=Sum('outstanding'))['sum_outstanding']

    if amount > total_debt:
        return Response({"error": "El monto de pago excede la deuda total."},
                        status=status.HTTP_400_BAD_REQUEST)

    payment_serializer = PaymentsSerializer(data=request_data)
    if payment_serializer.is_valid():

        payment_serializer.save()
        payment = payment_serializer.instance
        loan = payment_serializer.instance

        for loan_detail in payment_details:
            id = loan_detail["loan_id"]
            loan = Loans.objects.get(external_id=id)
            if loan.outstanding < loan_detail["payment_amount"]:
                return Response({"error": "El monto de pago por %s excede la deuda total."
                                 % loan_detail["payment_amount"]},
                                status=status.HTTP_400_BAD_REQUEST)

            loan.outstanding -= Decimal(loan_detail["payment_amount"])
            if loan.outstanding <= 0:
                loan.status = 4
                loan.outstanding = 0
            loan.save()
            # Escribir objeto de detalles de payment
            loan_detail["payment_id"] = payment.external_id

            payment_detail_serializer = PaymentDetailSerializer(data=loan_detail)
            if payment_detail_serializer.is_valid():
                payment_detail_serializer.save()
            else:
                return Response(payment_detail_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(payment_serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(payment_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)     
