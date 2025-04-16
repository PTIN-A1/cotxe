import asyncio
import json
import ssl
from ssl import SSLContext
from uuid import UUID

import certifi
import websockets

from peripherals.esp32 import Esp32
from peripherals.powertrain import Powertrain


class Car(Esp32, Powertrain):
    id: UUID
    ssl_context: SSLContext

    def __init__(
        self, id: UUID, serial_port: str, ignore: list[str], motor_interface: str
    ):
        self.id = id

        self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.load_verify_locations(certifi.where())

        self.connect_serial(serial_port, ignore)
        self.connect_powertain(motor_interface)

    async def connect_websocket(self, controller: str):
        async with websockets.connect(controller, ssl=self.ssl_context) as websocket:
            asyncio.create_task(self.send_location(websocket))

            while True:
                await asyncio.sleep(1)

    async def send_location(self, websocket):
        while True:
            try:
                location = await self.get_ap_rssis()
                await websocket.send(json.dumps({"location": location}))

            except Exception as e:
                print(f"Error sending location: {e}")  # TODO log
