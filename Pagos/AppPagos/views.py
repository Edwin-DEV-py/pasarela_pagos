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

#vista para crear orden
class OrderView(APIView):
    def post(self,request):
        
        #recibir el usuario desde el front
        user = request.data.get('user')
        
        cart_url = 'http://127.0.0.1:8000/api/cart/'
        cart_data = {
            "user": user
        }
        
        #hacer llamado a la api de carrito
        response = requests.get(cart_url, json=cart_data)
        
        #verificamos la respuesta
        if response.status_code == 200:
            items = response.json()
            
            #calcular el valor total, iva y subtotal
            total = sum(item['price'] + item['quantity'] for item in items)
            iva = total * 0.16
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
                    else:
                        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                response_data = {
                    'order':serializer.data,
                    'items':items
                }
                
            return Response(response_data, status=200)
        else:
            # Maneja el caso en que no se pueda obtener el carrito de compras correctamente
            return Response({'error': 'No se pudo obtener el carrito de compras'}, status=response.status_code)
        
