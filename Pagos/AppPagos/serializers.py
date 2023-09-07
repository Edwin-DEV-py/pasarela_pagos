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

#hacer el serializer de crear la orden y los productos de la orden       
class CreateOrderSerializer(serializers.ModelSerializer):
    items = CardOrderSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        
    def create(self,validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            CardOrder.objects.create(order=order, **item_data)
            
        return order
