# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir kafka-python requests

# Comando para ejecutar el script
CMD ["python", "sender.py"]
