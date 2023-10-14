from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer
from loans_app.models import Loans
from .serializer import CustomerSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum


@api_view(['POST'])
def create_customer(request):

    """
    Crea un nuevo cliente.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene los datos del cliente.

    Retorna:
    Response: Un objeto Response que contiene los detalles del cliente recién creado o los errores si la solicitud es inválida.

    """
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_customer(request):

    """
    Lista todos los clientes existentes.

    Parámetros:
    request (HttpRequest): La solicitud HTTP.

    Retorna:
    Response: Un objeto Response que contiene una lista de todos los clientes.

    """

    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_balance(request):

    """
    Obtiene el saldo disponible y la deuda total de un cliente.

    Parámetros:
    request (HttpRequest): La solicitud HTTP que contiene el ID externo del cliente.

    Retorna:
    Response: Un objeto Response que contiene el saldo disponible y la deuda total del cliente o un mensaje de error si el cliente no existe.

    """

    customer_id = request.GET.get('customer')
    customer = get_object_or_404(Customer, external_id=customer_id)

    if not customer:
        return Response({"error": "A 'customer' parameter is required."},
                        status=status.HTTP_400_BAD_REQUEST)
    # Calcular total deuda
    loans = Loans.objects.filter(customer=customer, status=2)
    total_debt = loans \
        .aggregate(sum_outstanding=Sum('outstanding'))['sum_outstanding']

    # Calcular monto disponible
    available_amount = customer.score - total_debt

    return Response({
        "total_debt": total_debt,
        "available_amount": available_amount
    })
