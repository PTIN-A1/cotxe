# Software del cotxe

![Static Badge](https://img.shields.io/badge/Python-3.9-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/DOCKER-28.0.4-gray?style=for-the-badge&logo=docker&logoColor=white&labelColor=%2336ace2) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue)

## Setup (cotxe físic):
- És necessari activar els busos necessaris per al cotxe. Utilitzeu
  ```bash
  rsetup
  ```
  Per activar els busos `I2C7`, `PWM0`, `PWM0` i `UART2`. (Overlays > Manage overlays)

- És necessari afegir l'usuari al grup `i2c` per que tingui accés als busos dels motors
  ```bash
  sudo usermod -aG i2c radxa
  ```

## Setup (general):

- Entra a l'entorn de desenvolupament per tenir totes les dependències instal·lades:
```bash
nix develop --experimental-features 'nix-command flakes'
```

- També pots optar per instal·lar directament les dependències de python:
```bash
pip install -r requeriments.txt
```

## Execució:
- Executa el codi del cotxe de la següent manera:
```bash
python3 -m src.cotxe_ptin.main
```
_Nota: Recorda que abans d'executar el codi del cotxe el servidor WebSocket ha d'estar escoltant. A més, per defecte el cotxe que s'executa és de tipus virtual._
_Si vols que el cotxe sigui de tipus físic, edita a main.py la línia de "car_type = os.getenv("CAR_TYPE", "virtual")", i canvia "virtual" per: physical_

## Execució amb un contenidor:
- Construeix la imatge de Docker amb la següent comanda:
```bash
docker build -t cotxe-ptin .
```
_Nota: Pots canviar el tipus de cotxe (physical/virtual) editant el fitxer "Dockerfile" i, al costat de "ENV CAR_TYPE=", posant (sense les cometes dobles) "physical" o "virtual"_

- Executa el contenidor amb la imatge de Docker
```bash
docker run --rm cotxe-ptin
```

_Nota: recorda que, com s'ha esmentat anteriorment, perquè el programa del cotxe funcioni el servidor WebSocket ha d'estar escoltant."_

## Guia d'estil:
- És necessari formatejar el codi amb autopep8 abans de enviar-lo a origin.
  ```bash
  autopep8 --in-place --recursive src/
  ```
- L'ordre dels imports és el següent:
  ```python
  import asyncio        # Primer els imports de la stdlib
  from uuid import UUID # Tots els imports en ordre alfabètic.
  
  import websockets     # Després els imports de llibreries externes

  import car            # Per últim els imports del propi projecte
  ```
