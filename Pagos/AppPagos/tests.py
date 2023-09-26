from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class OrderViewIntegrationTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_order_from_cart(self):
        # Datos de prueba
        user = 'usuario_prueba'

        # URL para crear una orden en el microservicio de órdenes
        create_order_url = reverse('order2') # Reemplaza con la URL real de tu microservicio de órdenes

        # Datos de prueba para crear una orden basada en el contenido del carrito
        create_order_data = {'user': user}

        # Enviar la solicitud POST para crear una orden basada en el carrito
        response = self.client.post(create_order_url, create_order_data, format='json')

        # Verificar que la respuesta sea un 200 OK o el código de estado esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
