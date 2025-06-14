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
from peripherals.powertrain.powertrain import Powertrain, State
from peripherals.powertrain.build import build_powertrain

from logic.navigation import Navigation


class Car:
    id: int
    ssl_context: SSLContext

    location: Location
    distance: Distance
    powertrain: Powertrain

    navigation: Navigation

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

        self.navigation = Navigation()

        log.info(f"Car {id} ready.")

    async def connect_websocket(self, controller: str):  # , ssl=self.ssl_context
        log.info(f"Connecting websocket to {controller}...")
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
                    "id": self.id,
                    "state": self.powertrain.state.value,
                    "coordinates": {
                        "x": x,
                        "y": y,
                    },
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
                log.info("Waiting for a new message from the websocket...")
                recieved = await websocket.recv()
                log.info(f"Recieved new message from websocket: {recieved}")
                route = json.loads(recieved)
                log.info("Parsed message to json succesfully.")

                if "path" not in route:
                    log.warn("Websocket message did not contain a path")
                    continue

                for waypoint in route["path"]["path"]:
                    direction = self.navigation.calculate_direction(
                        self.location.get(), waypoint
                    )
                    self.powertrain.move(direction)

                    while self.powertrain.state != State.Stopped:
                        await asyncio.sleep(0.2)
                        direction = self.navigation.calculate_direction(
                            self.location.get(), waypoint
                        )
                        self.powertrain.move(direction)

            except Exception as e:
                log.error(f"Failed to recieve from websocket: {e}")

    async def monitor_and_stop(self):
        while True:
            distance = self.distance.measure()

            if distance is not None:
                log.debug(f"Obstacle detected at {distance}")

                self.powertrain.direction(Powertrain.Direction.Stop)

            await asyncio.sleep(0.2)
