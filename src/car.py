import asyncio
import json
import logging as log
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
        log.info(f"Creating new Car instance with ID {id}.")
        self.id = id

        self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.load_verify_locations(certifi.where())

        self.connect_serial(serial_port, ignore)
        self.connect_powertain(motor_interface)
        log.info(f"Car {id} ready.")

    async def connect_websocket(self, controller: str):
        log.info(f"Connecting websocket to {controller}...")
        async with websockets.connect(controller, ssl=self.ssl_context) as websocket:
            log.info("Connected.")
            asyncio.create_task(self.send_location(websocket))
            asyncio.create_task(self.recieve_commands(websocket))

            while True:
                await asyncio.sleep(1)

        log.warn("Disconnected from websocket.")

    async def send_location(self, websocket):
        while True:
            try:
                location = await self.get_ap_rssis()

                log.debug("Sending location to websocket...")
                await websocket.send(json.dumps({"location": location}))
                log.debug("Location sent.")

            except Exception as e:
                log.error(f"Failed to send location to websocket: {e}")

    async def recieve_commands(self, websocket):
        while True:
            try:
                log.debug("Waiting for a new message from the websocket...")
                recieved = await websocket.recv()
                log.debug(f"Recieved new message from websocket: {recieved}")

                recieved = json.loads(recieved)
                log.debug("Parsed message to json succesfully.")

                # No match statement in python 3.9!!
                if recieved["command"] == "move":
                    direction = self.Direction.from_str(recieved["direction"])
                    self.move(direction)

            except Exception as e:
                log.error(f"Failed to recieve from websocket: {e}")
