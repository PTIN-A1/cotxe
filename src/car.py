import asyncio
import json
import logging as log
import ssl
from ssl import SSLContext

import certifi
import websockets

from peripherals.distance.distance import Distance
from peripherals.distance.build import to_subclass
from peripherals.powertrain.powertrain import Powertrain


class Car:
    id: str
    ssl_context: SSLContext

    distance: Distance
    # powertrain: Powertrain

    def __init__(
        self, id: str, serial_port: str, ignore: list[str], motor_interface: str
    ):
        log.info(f"Creating new Car instance with ID {id}.")
        self.id = id

        self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.load_verify_locations(certifi.where())

        self.distance = to_subclass()

        # self.connect_serial(serial_port, ignore)
        # self.connect_powertain(motor_interface)
        log.info(f"Car {id} ready.")

    async def connect_websocket(self, controller: str):
        log.info(f"Connecting websocket to {controller}...")
        async with websockets.connect(controller, ssl=self.ssl_context) as websocket:
            log.info("Connected.")
            asyncio.create_task(self.send_location(websocket))
            # asyncio.create_task(self.recieve_commands(websocket))

            while True:
                await asyncio.sleep(1)

        log.warn("Disconnected from websocket.")

    # async def send_location(self, websocket):
    #     while True:
    #         try:
    #             location = await self.get_ap_rssis()
    #
    #             log.debug("Sending location to websocket...")
    #             await websocket.send(json.dumps({"location": location}))
    #             log.debug("Location sent.")
    #
    #             await asyncio.sleep(0.5)  # Yield the websocket to other tasks
    #
    #         except Exception as e:
    #             log.error(f"Failed to send location to websocket: {e}")

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

    async def monitor_and_stop(self):
        while True:
            distance = self.get_distance()
            if distance is not None and distance < 40.0:
                log.debug(f"Obstacle a {distance} cm! Aturant motors.")
                self.move(direction="Stop")
            await asyncio.sleep(0.2)

    # async def obstacle_avoidance_loop(self):
    #     while True:
    #         distance = self.distance_sensor.measure()
    #         if distance is not None and distance < 40.0:
    #             log.debug(f"Obstacle detectat a {distance} cm! Aturant motors.")
    #             self.move(direction="Stop")
    #             await asyncio.sleep(0.5)
    #
    #             # Comencem a girar fins trobar camí lliure
    #             log.debug("Començant gir a la dreta...")
    #             self.move(direction="Right")
    #
    #             while True:
    #                 distance = self.get_distance()
    #                 if distance is not None and distance >= 40.0:
    #                     log.debug(
    #                         f"[Obstacle] Camí lliure ({distance} cm). Reprenent avanç."
    #                     )
    #                     break
    #                 await asyncio.sleep(0.2)
    #
    #             self.move(direction="Forward")
    #             self.move(direction="Forward")
            await asyncio.sleep(0.2)
