from django.urls import path
from .views import OrderView,PaymentView

urlpatterns = [
    path('order/<int:order_id>/', OrderView.as_view(),name='order'),
    path('order/', OrderView.as_view(),name='order2'),
    path('payment/', PaymentView.as_view(),name='pago'),
]