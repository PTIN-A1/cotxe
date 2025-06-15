# Software cotxe físic

![Static Badge](https://img.shields.io/badge/Python-3.11-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue) ![Static Badge](https://img.shields.io/badge/DOCKER-28.1.1-gray?style=for-the-badge&logo=docker&logoColor=white&labelColor=%2336ace2)

## Setup:
- S'ha d'instal·lar les dependències de python a l'entorn virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Es poden establir variables d'entorn per definir el ID del cotxe i el URI del websocket:
  ```bash
  export CAR_ID=<nombre_hexadecimal_id_cotxe> # Si no s'estableix, el valor per defecte és 0x346B9B94
  export CAR_CONTROLLER=<uri_websocket> # Si no s'estableix, el valor per defecte és ws://192.168.10.11:8765
  ```
- També es pot definir una variable d'entorn per indicar al cotxe que és la versió física:
  ```bash
  export ENVIRONMENT=physical
  ```
- I una per activar el logging:
  ```
  export CAR_LOG_LEVEL=<nivell_de_log> # Si no s'estableix, el valor per defecte és INFO. Nivells: DEBUG, INFO, WARNING, ERROR, CRITICAL
  ```
- El cotxe es pot enjagar amb la comanda següent:
  ```bash
  python src/main.py
  ```

# Software cotxe virtual

## Setup:

- Es poden establir variables d'entorn per definir paràmetres com el ID del cotxe i el URI del websocket a dins de "Env", al fitxer flake.nix.
  Com al cotxe físic, els valors per defecte són els següents:
  ```
  "CAR_ID=0x346B9B94"
  "CAR_CONTROLLER=ws://192.168.10.11:8765"
  ```

- Generar executable "result":
  ```bash
  nix --extra-experimental-features nix-command --extra-experimental-features flakes build
  ```

- Crear la imatge de Docker en format .tar.gz:
  ```bash
  ./result > cotxe-image.tar.gz
  ```
  
- Carregar imatge de Docker:
  ```bash
  docker load < cotxe-image.tar.gz
  ```

- Confirmar que la imatge s'ha carregat:
  ```bash
  docker images
  ```

- Executar cotxe virtual:
  ```bash
  docker run --rm cotxe-ptin:0.5.0
  ```

# Guia d'estil:
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
