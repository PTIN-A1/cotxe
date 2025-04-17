__version__ = "0.1.0"

import asyncio
import logging
import os
import time

from car import Car

logging.getLogger().setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())


async def main():
    id = os.getenv("CAR_ID", "00000000-0000-0000-0000-000000000000")
    serial_port = os.getenv("CAR_SERIAL_PORT", "/dev/ttyUSB0")
    ignore = [
        ap.strip() for ap in os.getenv("CAR_AP_IGNORE", "").split(",") if ap.strip()
    ]
    controller = os.getenv("CAR_CONTROLLER", "wss://localhost:8000")

    car = Car(id, serial_port, ignore, "/dev/i2c-7")
    await car.connect_websocket(controller)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
