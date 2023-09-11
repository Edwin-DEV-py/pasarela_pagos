from django.urls import path
from .views import OrderView

urlpatterns = [
    path('order/<str:user>/', OrderView.as_view(),name='order'),
]