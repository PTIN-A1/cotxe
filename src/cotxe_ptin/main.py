__version__ = "0.1.2"

import asyncio
import logging
import os
import time

from .car import Car

logging.getLogger().setLevel(level=os.getenv("CAR_LOG_LEVEL", "INFO").upper())


async def main():
    id = os.getenv("CAR_ID", "00000000-0000-0000-0000-000000000000")
    controller = os.getenv("CAR_CONTROLLER", "wss://echo.websocket.org")
    # Altre valor per defecte per a controller: "wss://localhost:8000"

    car = Car(id)
    await car.connect_websocket(controller)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
