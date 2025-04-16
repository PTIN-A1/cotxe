import asyncio
import json
from serial import Serial
import ssl
from ssl import SSLContext
from uuid import UUID
from ultrasonic import Ultrasonic
from motors import Motors

import certifi
import websockets


class Car:
    BAUD_RATE = 115200
    MEASUREMENT_START = ">>>MEASUREMENT>>>"
    MEASUREMENT_END = "<<<MEASUREMENT<<<"

    id: UUID
    ssl_context: SSLContext

    serial_port: Serial
    ignore: list[str]

    def __init__(self, id: UUID, serial_port: str, ignore: list[str]):
        self.id = id

        self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.load_verify_locations(certifi.where())

        self.serial_port = Serial(serial_port, self.BAUD_RATE, timeout=1)

        self.ignore = ignore
        PWM = Motors()

    async def connect(self, controller: str):
        async with websockets.connect(controller, ssl=self.ssl_context) as websocket:
            asyncio.create_task(self.send_location(websocket))

    async def send_location(self, websocket):
        while True:
            location = await self.get_ap_rssis()
            await websocket.send(json.dumps({"location": location}))

    async def get_ap_rssis(self) -> dict:
        access_points = []

        recieving = False

        while True:
            if self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode("utf-8").rstrip()

                # If we've reached the end of a measurement, return the measurement
                if line.startswith(self.MEASUREMENT_END):
                    return access_points

                # If we're not recieving, check if we should and jump to the next iteration
                if not recieving:
                    if line.startswith(self.MEASUREMENT_START):
                        recieving = True

                    continue

                # If we reached this point it means we're recieving a measurement
                measurement = json.loads(line)
                bssid = measurement.get("bssid")
                rssi = measurement.get("rssi")

                if bssid and rssi is not None and bssid not in self.ignore:
                    access_points.append(
                        {
                            "bssid": bssid,
                            "rssi": rssi,
                        }
                    )

    def stop_car(self):
        PWM.set_motor_model(0,0,0,0);
        
    def move_forward(self):
        PWM.set_motor_model(1000, 1000, 1000, 1000);
        
    def move_backwards():
        PWM.set_motor_model(-1000,-1000,-1000,-1000)
        
    def move_left():
        PWM.set_motor_model(-1000,-1000,1000,1000)
        
    def move_right():
        PWM.set_motor_model(1000,1000,-1000,-1000)
    
