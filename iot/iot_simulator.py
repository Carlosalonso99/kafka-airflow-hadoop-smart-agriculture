# Paso 1: Crear un script para conectar Kafka con Power BI

# Instalación de dependencias necesarias:
# Ejecuta este comando en tu terminal para instalar Kafka-Python y Requests
# pip install kafka-python requests

from kafka import KafkaConsumer
import json
import requests
import threading
import time

# Paso 2: Definir los parámetros de configuración

# Kafka Configuration
KAFKA_TOPIC = 'sensor-data'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'

# Power BI Configuration
POWER_BI_PUSH_URL = 'https://api.powerbi.com/beta/68519e48-83f3-435f-a38a-1a7aa77ba987/datasets/60a6a0aa-13c8-4968-a240-8106d50cd59a/rows?experience=power-bi&key=CoenFYHO3F6ztIzxJpVchwbOGiVgfmX7RujDGrLyChkLJvtro%2FFLaFqyGnveXgqlXL6UL9biAJuLA8iW44Zvzg%3D%3D'

# Paso 3: Crear el consumidor de Kafka

class KafkaConsumerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.consumer = None
        self.initialize_consumer()

    def initialize_consumer(self):
        print("Inicializando el consumidor de Kafka...")
        while self.consumer is None:
            try:
                self.consumer = KafkaConsumer(
                    KAFKA_TOPIC,
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    api_version=(2, 7, 0)  # Especificar la versión del API para mejorar la compatibilidad
                )
                print("Consumidor de Kafka inicializado correctamente.")
            except Exception as e:
                print(f"Error al inicializar el consumidor de Kafka: {str(e)}")
                time.sleep(5)
                print("Reintentando la conexión al consumidor de Kafka...")

    def run(self):
        if self.consumer is None:
            print("Consumidor de Kafka no disponible. Finalizando el hilo.")
            return

        print("Iniciando la lectura de mensajes desde Kafka...")
        try:
            for message in self.consumer:
                data = message.value
                print(f"Mensaje recibido desde Kafka: {data}")
                # Verificar el contenido del mensaje recibido
                if isinstance(data, dict):
                    print("El mensaje recibido es un diccionario JSON válido.")
                    # Paso 4: Enviar los datos a Power BI cuando se reciban desde Kafka
                    self.send_to_power_bi(data)
                else:
                    print(f"El mensaje recibido no es un diccionario válido: {data}")
        except Exception as e:
            print(f"Error al leer mensajes desde Kafka: {str(e)}")
            time.sleep(5)
            print("Reintentando la conexión al consumidor de Kafka...")
            self.initialize_consumer()
            self.run()

    def send_to_power_bi(self, data):
        print("Preparando los datos para enviar a Power BI...")
        payload = [{
            "device_id": data.get("device_id", "unknown"),
            "timestamp": data.get("timestamp", "unknown"),
            "temperature": data.get("temperature", 0.0),
            "humidity": data.get("humidity", 0.0),
            "light": data.get("light", 0.0)
        }]  # La API de Power BI espera una lista de filas
        headers = {'Content-Type': 'application/json'}
        try:
            print(f"Enviando los siguientes datos a Power BI: {payload}")
            response = requests.post(POWER_BI_PUSH_URL, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                print("Datos enviados exitosamente a Power BI")
            else:
                print(f"Error al enviar datos a Power BI: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Excepción al enviar datos a Power BI: {str(e)}")

# Paso 5: Iniciar el consumidor de Kafka

if __name__ == '__main__':
    print("Iniciando el hilo del consumidor de Kafka...")
    kafka_consumer_thread = KafkaConsumerThread()
    kafka_consumer_thread.start()
    print("Hilo del consumidor de Kafka iniciado.")
