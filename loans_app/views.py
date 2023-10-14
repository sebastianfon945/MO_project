from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Loans
from customers_app.models import Customer
from .serializer import LoansSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum


@api_view(['POST'])
def create_loan(request):

    """
    Crea un nuevo préstamo asociado a un cliente.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene los datos del préstamo.

    Retorna:
    Response: Un objeto Response que contiene los detalles del préstamo recién creado o los errores si la solicitud es inválida.

    """

    customer_external_id = request.data.get('customer')

    # Check if the associated customer exists
    try:
        customer = Customer.objects.get(external_id=customer_external_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer does not exist."},
                        status=status.HTTP_400_BAD_REQUEST)
    # Check if the associated customer is active
    if customer.status == 2:
        return Response({"error": "The associated customer is not active."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check if total_outstanding is greater than customer score
    loans = get_loans_by_customer(Customer, customer_external_id)
    total_outstanding = loans \
        .aggregate(sum_outstanding=Sum('outstanding'))['sum_outstanding'] or 0

    if total_outstanding >= customer.score:
        error_msg = ("El total de los préstamos pendientes "
                     "excede el límite de crédito permitido")
        return Response({"error": error_msg},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check request body
    serializer = LoansSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_loans(request):

    """
    Lista todos los préstamos existentes.

    Parámetros:
    request (HttpRequest): La solicitud HTTP.

    Retorna:
    Response: Un objeto Response que contiene una lista de todos los préstamos.

    """

    # Get all created loans
    loans = Loans.objects.all()
    serializer = LoansSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def loan_by_id(request):

    """
    Obtiene un préstamo por su ID externo.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene el ID externo del préstamo.

    Retorna:
    Response: Un objeto Response que contiene los detalles del préstamo correspondiente al ID externo proporcionado o un mensaje de error si el préstamo no existe.

    """

    loan_id = request.GET.get('external_id')
    try:
        loan = Loans.objects.get(external_id=loan_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer does not exist."},
                        tatus=status.HTTP_400_BAD_REQUEST)
    serializer = LoansSerializer(loan)
    return Response(serializer.data)


@api_view(['GET'])
def loans_by_customer(request):

    """
    Lista todos los préstamos de un cliente específico.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene el ID externo del cliente.

    Retorna:
    Response: Un objeto Response que contiene una lista de todos los préstamos asociados al cliente o un mensaje de error si el cliente no existe.

    """

    customer_id = request.GET.get('customer')

    # Check url customer param
    if not customer_id:
        return Response({"error": "A 'customer' parameter is required."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Get all Loans by Customer
    loans = get_loans_by_customer(Customer, customer_id)
    serializer = LoansSerializer(loans, many=True)
    return Response(serializer.data)


def get_loans_by_customer(Customer, customer_id):

    """
    Obtiene todos los préstamos de un cliente específico.

    Parámetros:
    Customer: El modelo de cliente.
    customer_id (str): El ID externo del cliente.

    Retorna:
    QuerySet: Un conjunto de consultas que contiene todos los préstamos asociados al cliente.

    """

    # Get all Loans by Customer
    customer = get_object_or_404(Customer, external_id=customer_id)
    loans = Loans.objects.filter(customer=customer)
    return loans
