import json
import time
import random
from confluent_kafka import Producer

# Configurar el productor de Kafka
producer = Producer({
    'bootstrap.servers': 'localhost:29092'
})

# Definir las características de los sensores
sensor_types = ['temperature', 'humidity', 'light']
device_ids = ['sensor_1', 'sensor_2', 'sensor_3']

def generate_sensor_data():
    """
    Genera datos simulados para diferentes tipos de sensores.
    """
    sensor_data = {
        'device_id': random.choice(device_ids),
        'timestamp': int(time.time()),
        'temperature': round(random.uniform(10.0, 35.0), 2),
        'humidity': round(random.uniform(30.0, 90.0), 2),
        'light': round(random.uniform(300, 800), 2)
    }
    return sensor_data

def delivery_report(err, msg):
    """
    Reporte de entrega de mensajes.
    """
    if err is not None:
        print(f'Error al entregar el mensaje: {err}')
    else:
        print(f'Mensaje entregado a {msg.topic()} [{msg.partition()}]')

def send_data():
    """
    Enviar datos simulados a Kafka en intervalos regulares.
    """
    while True:
        data = generate_sensor_data()
        print(f'Enviando datos: {data}')
        producer.produce('sensor-data', value=json.dumps(data), callback=delivery_report)
        producer.poll(1)  # Esperar y procesar la cola de mensajes
        time.sleep(2)  # Enviar cada 2 segundos

if __name__ == '__main__':
    send_data()
