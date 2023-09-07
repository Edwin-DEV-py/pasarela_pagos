from rest_framework import serializers
from .models import Payment,Order,CardOrder

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CardOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardOrder
        fields = '__all__'
