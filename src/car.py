import asyncio
import json
import logging as log
import requests # temporal, només per fer proves
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
        self.powertrain = build_powertrain(self.location)

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
                 # car_location = await self.get_ap_rssis()
    
                 log.debug("Sending location to websocket...")
                 # await websocket.send(json.dumps({"location": car_location}))
                 log.debug("Location sent.")
                 x, y = self.location.get()
                 print(f"Ubicació actual: {x} {y}")
                 
                 await asyncio.sleep(1)  # Yield the websocket to other tasks
    
             except Exception as e:
                 log.error(f"Failed to send location to websocket: {e}")

    async def recieve_commands(self, websocket):
        final = 0
        while True:
            try:
                # log.debug("Waiting for a new message from the websocket...")
                # recieved = await websocket.recv()
                # log.debug(f"Recieved new message from websocket: {recieved}")

                # recieved = json.loads(recieved)
                # log.debug("Parsed message to json succesfully.")

                # No match statement in python 3.9!!
                # if recieved["command"] == "move":
                #    direction = self.Direction.from_str(recieved["direction"])
                #    self.move(direction)
                if final == 1:
                    break
                
                url = "http://127.0.0.1:8000/path"
                data = {
                    "start": [0.5015634772, 0.3986866792],
                    "goal": [0.5109443402, 0.3367729831]
                }

                respuesta = requests.post(url, json=data)
                ruta = respuesta.json()
                if "path" in ruta:
                    print("Ruta trobada, comencem...")
                    for punto in ruta["path"]:
                        x, y = punto
                        # print(f"Anant a ({x}, {y})")
                        self.powertrain.move(punto)
                        await asyncio.sleep(1)  # Emular temps de desplaçament
                    final = 1
                else:
                    print("Ruta no trobada")

                x, y = self.location.get()
                print(f"Ubicació actual: {x} {y}")
                 
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
