from django.db import models

#estado del pago
status_content = (
    ('Nuevo','Nuevo'),
    ('Aceptado','Aceptado'),
    ('Completado','Completado'),
    ('Cancelado','Cancelado'),
)

#modelo de pago
class Payment(models.Model):
    payment_id = models.AutoField(unique=True,primary_key=True)
    id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
#modelo de orden
class Order(models.Model):
    order_id = models.AutoField(unique=True,primary_key=True)
    user = models.CharField(max_length=100)
    #payment = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    order_total = models.FloatField()
    iva = models.FloatField()
    status = models.CharField(max_length=20, choices=status_content, default='Nuevo')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def get_url(self): #devuelve una url para poder ver el detalle mas adelante
        return reversed('orden_detail',args=[self.order_note])
    
#modelo de cartas por orden
class CardOrder(models.Model):
    user = models.CharField(max_length=100)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    id_carta = models.CharField(max_length=24)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def sub_total(self):
        return self.price * self.quantity