# DON'T USE THIS FILE

# Imatge base
FROM python:3.12-slim

# Establir directori de treball
WORKDIR /app

# Copiar fitxers necessaris (comandes executades a dins de /app)
COPY requirements.txt .
COPY setup.py .
COPY src/ ./src/

# Instal·lar dependències
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

# Tipus de cotxe (physical/virtual)
ENV ENVIRONMENT=virtual

# Servidor WebSocket del Controller
# ENV CAR_CONTROLLER=wss://198.168.10.11:8765

# Punt d'entrada
CMD ["python", "-m", "cotxe_ptin.main"]

