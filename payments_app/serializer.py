from rest_framework import serializers
from .models import Payments, PaymentDetail


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class PaymentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetail
        fields = '__all__'
