# Imatge base
FROM python:3.12-slim

# Establir directori de treball
WORKDIR /app

# Copiar fitxers necessaris
COPY requirements.txt .
COPY setup.py .
COPY src/ ./src/

# Instal·lar dependències
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

# Tipus de cotxe (physical/virtual)
ENV CAR_TYPE=virtual

# Punt d'entrada
CMD ["python", "-m", "cotxe_ptin.main"]

