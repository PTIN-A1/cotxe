import os

from .location import Location
from .esp32 import Esp32


class PhysicalLocation(Location):
    esp32: Esp32
    # locator: RssiLocator

    def __init__(self):
        serial_port = os.getenv("CAR_SERIAL_PORT", "/dev/ttyUSB0")
        ignore = [
            ap.strip() for ap in os.getenv("CAR_AP_IGNORE", "").split(",") if ap.strip()
        ]

        self.esp32 = Esp32().connect_serial(serial_port, ignore)

    def measure(self):
        measure = self.esp32.get_ap_rssis()
