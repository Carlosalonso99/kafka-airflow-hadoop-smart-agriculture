# README: Guía de Inicio Rápido para Kafka y Airflow

## Introducción
Este proyecto incluye un entorno de orquestación de datos utilizando Kafka, Airflow, y Hadoop. El archivo `docker-compose.yml` configura todos los servicios necesarios. Esta guía proporciona los pasos necesarios para poner en marcha los contenedores, crear un topic en Kafka, y ejecutar el scheduler de Airflow.

## Requisitos Previos
- Docker y Docker Compose instalados en tu máquina.
- Puertos disponibles para los servicios: 2181 (Zookeeper), 9092 (Kafka), 8085 (Airflow Web), y otros puertos necesarios para Hadoop.

## Iniciar los Contenedores
Para poner en marcha el entorno completo, ejecuta el siguiente comando desde la carpeta donde se encuentra el archivo `docker-compose.yml`:

```bash
docker-compose up -d
```
Este comando iniciará todos los servicios en segundo plano. Los servicios incluyen:
- Zookeeper para la coordinación de Kafka
- Kafka Broker
- Airflow para la orquestación de flujos de trabajo
- Hadoop Namenode y Datanode

## Verificar los Contenedores
Una vez iniciados los contenedores, verifica que estén corriendo:

```bash
docker-compose ps
```
Deberías ver todos los servicios en estado "Up".

## Crear el Topic en Kafka
El topic `sensor-data` se debe crear manualmente si no se crea automáticamente. Para hacerlo, sigue estos pasos:

1. Ejecuta el siguiente comando para acceder al contenedor de Kafka:

    ```bash
    docker exec -it kafka-airflow-hadoop-smart-agriculture-kafka-1 /bin/bash
    ```

2. Dentro del contenedor de Kafka, crea el topic `sensor-data`:

    ```bash
    kafka-topics --create --topic sensor-data --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
    ```

3. Puedes listar los topics existentes para verificar que se haya creado correctamente:

    ```bash
    kafka-topics --list --bootstrap-server kafka:9092
    ```

## Copiar la Carpeta `dags` al Contenedor de Airflow
Para asegurarte de que los DAGs se copien correctamente al contenedor de Airflow, sigue estos pasos:

1. Copia la carpeta `dags` al contenedor de Airflow:

    ```bash
    docker cp ./dags kafka-airflow-hadoop-smart-agriculture-airflow-1:/opt/airflow/
    ```

2. Accede al contenedor de Airflow como root:

    ```bash
    docker exec -it --user root kafka-airflow-hadoop-smart-agriculture-airflow-1 /bin/bash
    ```

3. Una vez dentro del contenedor, instala `kafka-python`:

    ```bash
    apt-get update && apt-get install iputils-ping -y
    pip install kafka-python
    ```

4. Cambia al usuario `airflow` si es necesario:

    ```bash
    su airflow
    ```

5. Reinicia el contenedor de Airflow para que detecte los cambios en los DAGs:

    ```bash
    docker restart kafka-airflow-hadoop-smart-agriculture-airflow-1
    ```

## Iniciar el Scheduler de Airflow
Para que los DAGs se ejecuten automáticamente en Airflow, es necesario iniciar el scheduler. El scheduler se puede iniciar directamente dentro del contenedor de Airflow.

1. Accede al contenedor de Airflow:

    ```bash
    docker exec -it kafka-airflow-hadoop-smart-agriculture-airflow-1 /bin/bash
    ```

2. Inicia el scheduler:

    ```bash
    airflow scheduler
    ```

El scheduler debe seguir corriendo en segundo plano para gestionar las ejecuciones de los DAGs.

## Acceder a la UI de Airflow
Una vez que el servidor web de Airflow esté en funcionamiento, puedes acceder a la interfaz web en: [http://localhost:8085](http://localhost:8085)

Desde la UI de Airflow, podrás ver los DAGs que hayas definido, ejecutarlos manualmente, y monitorear su estado.

## Solución de Problemas Comunes
- **Kafka no se puede conectar al broker:** Verifica que el contenedor de Kafka esté en funcionamiento y que las variables de entorno en el archivo `docker-compose.yml` estén configuradas correctamente.
- **Airflow no detecta los DAGs:** Asegúrate de que los DAGs estén en la carpeta correcta (`dags`) y que el volumen esté montado correctamente en `/opt/airflow/dags` dentro del contenedor de Airflow.
- **Error de módulo faltante `kafka`:** Si obtienes el error `ModuleNotFoundError: No module named 'kafka'`, asegúrate de que el módulo `kafka-python` esté instalado en el contenedor de Airflow.

## Detener los Contenedores
Para detener todos los servicios, ejecuta:

```bash
docker-compose down
```
Esto detendrá y eliminará los contenedores que se crearon.

## Conclusión
Esta guía te proporciona las instrucciones para poner en marcha los servicios necesarios para gestionar datos mediante Kafka y Airflow. Asegúrate de seguir cada paso y verifica el estado de cada servicio en caso de problemas.

