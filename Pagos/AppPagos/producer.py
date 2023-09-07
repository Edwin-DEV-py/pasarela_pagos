import pika, json

#conexion con CloudAMQP
params = pika.URLParameters('amqps://rlvgzuul:IR8L9U8f_vzjLAF0P4gtt9ALoMC4Q8W7@jaragua.lmq.cloudamqp.com/rlvgzuul')
connection = pika.BlockingConnection(params)
channel = connection.channel()
print('conectado')
#funcion para publicar el mensaje
def publish(method,body):
    properties = pika.BasicProperties(method,delivery_mode=2) #anadir el delivery_mode=2 para que sea persistente
    channel.basic_publish(exchange='',routing_key='carrito',body=json.dumps(body), properties=properties)
