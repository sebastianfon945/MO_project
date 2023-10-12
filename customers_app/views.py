from rest_framework import viewsets, mixins
from .models import Customer
from loans_app.models import Loans
from .serializer import CustomerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def get_balance(self, request, pk=None):
        customer = self.get_object()
        import pdb; pdb.set_trace()
        # Calcular total deuda
        # total_debt = Loans.objects.filter(customer=customer, status=1).aggregate(total=models.Sum('outstanding'))['total'] or 0

        # Calcular monto disponible
        # available_amount = customer.score - total_debt

        return Response({
            "total_debt": "test",
            "available_amount": "available_amount"
        })

# Create your views here.
