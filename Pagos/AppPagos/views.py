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
        user = request.data.get('user')
        
        cart_url = 'http://127.0.0.1:8000/api/cart/'
        cart_data = {
            "user": user
        }
        response = requests.get(cart_url, json=cart_data)
        if response.status_code == 200:
            items = response.json()
            
            order_items = [item['id_carta'] for item in items]
            
            total = sum(item['price'] + item['quantity'] for item in items)
            iva = total * 0.16
            subfinal = total
            final = total + iva
            
            data = {
                'user':user,
                'order_total':total,
                'iva':iva,
                'data':'hola'
            }
            
            serializer = OrderSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()

                response_data = {
                    'order':serializer.data,
                    'items':order_items
                }
                
            return Response(response_data, status=200)
        else:
            # Maneja el caso en que no se pueda obtener el carrito de compras correctamente
            return Response({'error': 'No se pudo obtener el carrito de compras'}, status=response.status_code)
        
