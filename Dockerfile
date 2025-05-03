# Imagen base
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY setup.py .
COPY src/ ./src/

# Instalar las dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

ENV CAR_TYPE=virtual

# Comando por defecto (ajusta según tu paquete y punto de entrada)
CMD ["python", "-m", "cotxe_ptin.main"]

