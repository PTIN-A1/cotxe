__version__ = "0.2.0"

import asyncio
import logging
import os
import time

from car import Car

logging.getLogger().setLevel(level=os.getenv("CAR_LOG_LEVEL", "INFO").upper())


async def main():
    id = os.getenv("CAR_ID", "00000000-0000-0000-0000-000000000000")
    controller = os.getenv("CAR_CONTROLLER", "ws://192.168.10.11:8765")

    car = Car(id)
    await car.connect_websocket(controller)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
