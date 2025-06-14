# Software cotxe físic

<<<<<<< HEAD
![Static Badge](https://img.shields.io/badge/Python-3.9-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue)
=======
![Static Badge](https://img.shields.io/badge/Python-3.11-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue)
>>>>>>> a713f028ad786e48361dc06b97ac86277a6993d3

## Setup:
- S'ha d'instal·lar les dependències de python a l'entorn virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requeriments.txt
  ```
- Es poden establir variables d'entorn per definir el ID del cotxe i el URI del websocket:
  ```bash
  export CAR_ID=<nombre_hexadecimal_id_cotxe> # Si no s'estableix, el valor per defecte és 0x346B9B94
  export CAR_CONTROLLER=<uri_websocket> # Si no s'estableix, el valor per defecte és ws://192.168.10.11:8765
  ```
<<<<<<< HEAD

- S'ha d'instal·lar les dependències de python
=======
- També es pot definir una variable d'entorn per indicar al cotxe que és la versió física:
>>>>>>> a713f028ad786e48361dc06b97ac86277a6993d3
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
