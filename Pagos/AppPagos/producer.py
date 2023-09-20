import pika, json

params = pika.URLParameters('amqps://pimhdfyz:v79_lwTMTMNkSRg3qgGxbQC1nD2y6ivM@jaragua.lmq.cloudamqp.com/pimhdfyz')
connection = pika.BlockingConnection(params)
channel = connection.channel()
print('conectado')
#funcion para publicar el mensaje
def publish(method, body):
    try:
        properties = pika.BasicProperties(method, delivery_mode=2)  # Añade delivery_mode=2 para que sea persistente
        channel.basic_publish(exchange='', routing_key='carrito', body=json.dumps(body), properties=properties)
        print('Mensaje publicado con éxito')
    except Exception as e:
        print(f'Error al publicar el mensaje: {str(e)}')

#canal dos        
params2 = pika.URLParameters('amqps://pimhdfyz:v79_lwTMTMNkSRg3qgGxbQC1nD2y6ivM@jaragua.lmq.cloudamqp.com/pimhdfyz')
connection2 = pika.BlockingConnection(params2)
channel2 = connection2.channel()
print('conectado2')
#funcion para publicar el mensaje
def publish2(method, body):
    try:
        properties2 = pika.BasicProperties(method, delivery_mode=2)  # Añade delivery_mode=2 para que sea persistente
        channel2.basic_publish(exchange='', routing_key='perfil', body=json.dumps(body), properties=properties2)
        print('Mensaje publicado con éxito')
    except Exception as e:
        print(f'Error al publicar el mensaje: {str(e)}')
        