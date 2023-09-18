import pika, json

#conexion con CloudAMQP
params = pika.URLParameters('amqps://hjfmgkct:to4kbvFm2IJXwuHRSU7KeS4xaYI11C1f@jackal.rmq.cloudamqp.com/hjfmgkct')
connection = pika.BlockingConnection(params)
channel = connection.channel()
print('conectado')
#funcion para publicar el mensaje
def publish(method,body):
    properties = pika.BasicProperties(method,delivery_mode=2) #anadir el delivery_mode=2 para que sea persistente
    channel.basic_publish(exchange='',routing_key='carrito2',body=json.dumps(body), properties=properties)


#segunda conexion

params2 = pika.URLParameters('amqps://augowwbq:8t-grsKLXggpPsDjMb-YH9sLf7bBTzRm@jaragua.lmq.cloudamqp.com/augowwbq')
connection2 = pika.BlockingConnection(params2)
channel2 = connection2.channel()
print('conectado2')
#funcion para publicar el mensaje
def publish2(method,body):
    properties2 = pika.BasicProperties(method,delivery_mode=2) #anadir el delivery_mode=2 para que sea persistente
    channel2.basic_publish(exchange='',routing_key='perfil',body=json.dumps(body), properties=properties2)
