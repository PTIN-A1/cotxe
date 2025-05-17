import asyncio
import json
import logging as log
import ssl
from ssl import SSLContext

import certifi
import websockets

from peripherals.location.location import Location
from peripherals.location.build import build_location
from peripherals.distance.distance import Distance
from peripherals.distance.build import build_distance
from peripherals.powertrain.powertrain import Powertrain
from peripherals.powertrain.build import build_powertrain


class Car:
    id: str
    ssl_context: SSLContext

    location: Location
    distance: Distance
    powertrain: Powertrain

    def __init__(
        self,
        id: str,
    ):
        log.info(f"Creating new Car instance with ID {id}.")
        self.id = id

        self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.load_verify_locations(certifi.where())

        self.location = build_location()
        self.distance = build_distance()
        self.powertrain = build_powertrain()

        log.info(f"Car {id} ready.")

    async def connect_websocket(self, controller: str):
        log.info(f"Connecting websocket to {controller}...")
        # , ssl=self.ssl_context
        async with websockets.connect(controller) as websocket:
            log.info("Connected.")
            asyncio.create_task(self.send_location(websocket))
            asyncio.create_task(self.get_route(websocket))

            while True:
                await asyncio.sleep(1)

        log.warn("Disconnected from websocket.")

    async def send_location(self, websocket):
        while True:
            try:
                x, y = self.location.get()

                data = {
                    "coordinates": {
                        "x": x,
                        "y": y,
                    }
                }

                log.debug("Sending location to websocket...")
                await websocket.send(json.dumps(data))
                log.debug("Location sent.")

                await asyncio.sleep(1)

            except Exception as e:
                log.error(f"Failed to send location to websocket: {e}")

    async def get_route(self, websocket):
        while True:
            try:
                log.debug("Waiting for a new message from the websocket...")
                recieved = await websocket.recv()
                log.debug(f"Recieved new message from websocket: {recieved}")
                route = json.loads(recieved)
                log.debug("Parsed message to json succesfully.")

                if "path" not in route:
                    log.warn("Websocket message did not contain a path")
                    continue

                for [x, y] in route["path"]:
                    direction = Powertrain.Direction.Stop  # TODO
                    self.powertrain.move(direction)

                    await asyncio.sleep(0.2)

                self.powertrain.change_status("Available")

            except Exception as e:
                log.error(f"Failed to recieve from websocket: {e}")

    async def monitor_and_stop(self):
        while True:
            distance = self.distance.measure()

            if distance is not None:
                log.debug(f"Obstacle detected at {distance}")

                self.powertrain.direction(Powertrain.Direction.Stop)

            await asyncio.sleep(0.2)
