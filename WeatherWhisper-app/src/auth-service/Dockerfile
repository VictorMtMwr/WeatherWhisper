FROM python:3.12.7-alpine  

# Instalar dependencias del sistema
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    unixodbc \
    unixodbc-dev 

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo el requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt requirements.txt

# Actualizar pip y luego instalar las dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto necesario
EXPOSE 5003

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
