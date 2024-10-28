import json
import time
import random
from kafka import KafkaProducer

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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

def send_data():
    """
    Enviar datos simulados a Kafka en intervalos regulares.
    """
    while True:
        data = generate_sensor_data()
        print(f'Enviando datos: {data}')
        producer.send('sensor-data', value=data)
        time.sleep(2)  # Enviar cada 2 segundos

if __name__ == '__main__':
    send_data()
