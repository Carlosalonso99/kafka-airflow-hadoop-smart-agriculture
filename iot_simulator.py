from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
import json
import logging
from hdfs import InsecureClient

# Configurar el logger para que las alertas se muestren en la UI de Airflow
log = logging.getLogger(__name__)

# Definir el DAG y sus parámetros
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 28),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=2),
}

dag = DAG(
    'monitor_sensor_data',
    default_args=default_args,
    description='Monitorea datos de sensores IoT y genera alertas si es necesario',
    schedule_interval=timedelta(minutes=2),
)

# Función para consumir datos de Kafka y verificar las condiciones de alerta
def consume_and_check_alerts(**kwargs):
    consumer = KafkaConsumer(
        'sensor-data',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    # Cliente HDFS
    hdfs_client = InsecureClient('http://namenode:9870', user='hadoop')
    
    alert_generated = False
    start_time = datetime.now()

    # Definir un tiempo máximo para el consumo (por ejemplo, 1 minuto)
    max_duration = timedelta(minutes=1)

    for message in consumer:
        sensor_data = message.value
        print(f'Recibido: {sensor_data}')
        
        # Verificar las condiciones
        temperature = sensor_data.get('temperature')
        humidity = sensor_data.get('humidity')

        # Listado de alertas
        alerts = []

        if temperature > 30:
            alert_message = f'Alerta: Temperatura alta detectada ({temperature}°C)'
            print(alert_message)
            alerts.append(alert_message)
            alert_generated = True
        
        if humidity < 40:
            alert_message = f'Alerta: Humedad baja detectada ({humidity}%)'
            print(alert_message)
            alerts.append(alert_message)
            alert_generated = True

        # Guardar alertas en HDFS
        if alerts:
            try:
                with hdfs_client.write('/alerts/alerts.log', append=True, encoding='utf-8') as f:
                    for alert in alerts:
                        f.write(f"{datetime.now()}: {alert}\n")
            except Exception as e:
                log.error(f"Error al escribir en HDFS: {e}")

        # Terminar si se ha alcanzado el tiempo máximo de ejecución
        if datetime.now() - start_time > max_duration:
            break

    # Marcar la tarea como success solo si se generó al menos una alerta
    if alert_generated:
        log.info("Se generaron alertas, tarea completada exitosamente.")
    else:
        raise ValueError("No se generaron alertas durante la ejecución.")

# Tarea para consumir datos y verificar alertas
check_alerts_task = PythonOperator(
    task_id='check_alerts',
    python_callable=consume_and_check_alerts,
    provide_context=True,
    dag=dag,
)

# Definir la secuencia de tareas
check_alerts_task
