from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment,Order,CardOrder
from .serializers import PaymentSerializer,OrderSerializer,CardOrderSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
import requests
from .producer import publish2,publish

#vista para crear orden
class OrderView(APIView):
    def get(self,request,order_id):
        #order_id = request.data.get('order_id')
        
        order = Order.objects.get(order_id=order_id)
        itemOrder = CardOrder.objects.filter(order=order_id)
        
        serializer3 = OrderSerializer(order)
        serializer4 = CardOrderSerializer(itemOrder,many=True)
        
        response_data = {
            'order_id':serializer3.data,
            'Items':serializer4.data
        }
        return Response(response_data)
    
    def post(self,request):
        
        #recibir el usuario desde el front
        user = request.data.get('user')
        print('Usuario recibido:', user)
        
        cart_url = 'http://127.0.0.1:8001/api/cart/'
        cart_data = {
            "user": user
        }
        
        #hacer llamado a la api de carrito
        response = requests.get(cart_url, json=cart_data)
        
        #verificamos la respuesta
        if response.status_code == 200:
            items = response.json()
            
            #calcular el valor total, iva y subtotal
            total = sum(item['price'] * item['quantity'] for item in items)
            iva = total * 0.19
            final = total + iva
            
            #datos para la orden de compra
            data = {
                'user':user,
                'order_total':final,
                'iva':iva
            }
            
            serializer = OrderSerializer(data=data)
            #guardar el serializer y mostrar la respuesta
            if serializer.is_valid():
                order = serializer.save()
                order_data = OrderSerializer(order).data #serializamos la respuesta
                
                #para cada carta del carrito que estaba a la hora de la orden se anade a la base de datos y se le asigna a la orden de compra
                for i in items:
                    data2={
                        'user':user,
                        'order': order_data['order_id'],
                        'id_carta':i['id_carta'],
                        'quantity':i['quantity'],
                        'price':i['price']
                    }
                    
                    #se serializa la rsepuesta y se guardan las cartas
                    serializer2 = CardOrderSerializer(data=data2)

                    if serializer2.is_valid():
                        serializer2.save()
                        publish('vaciar_carrito',user)
                    else:
                        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                'order':serializer.data,
                'items':items
            }
                
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Maneja el caso en que no se pueda obtener el carrito de compras correctamente
            return Response({'error': 'No se pudo obtener el carrito de compras'}, status=response.status_code)
        
#Guardar el pago
class PaymentView(APIView):
    def post(self,request):
        user = request.data.get('user')
        order = request.data.get('order_id')
        total = request.data.get('order_total')
        status = request.data.get('status')
        paymentID = request.data.get('paymentID')
        print(user,order,total,status,paymentID)
        
        data = {
            'user': user,
            'id' :order,
            'payment_method':paymentID,
            'amount_id': total,
            'status':status #esto lo devuelve paypal
        }
        
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            publish2('agregar-perfil',{'user': user, 'order_id': order})
        
        return Response(serializer.data)
        
        
