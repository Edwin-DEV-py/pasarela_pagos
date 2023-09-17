from django.urls import path
from .views import OrderView

urlpatterns = [
    path('order/<int:order_id>/', OrderView.as_view(),name='order'),
]