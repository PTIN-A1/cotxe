# Software cotxe físic

![Static Badge](https://img.shields.io/badge/Python-3.11-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue)

## Setup:
- S'ha d'instal·lar les dependències de python a l'entorn virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requeriments.txt
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
