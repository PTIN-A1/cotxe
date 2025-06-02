import threading
import os

import joblib

from peripherals.location.location import Location
from peripherals.location.esp32 import Esp32


class PhysicalLocation(Location):
    esp32: Esp32
    DEFAULT_RSSI: float = -100.0

    def __init__(self):
        serial_port = os.getenv("CAR_SERIAL_PORT", "/dev/ttyUSB0")
        model_path = os.getenv("LOCATION_MODEL_PATH", "assets/position_model.pkl")

        ignore = [
            ap.strip() for ap in os.getenv("CAR_AP_IGNORE", "").split(",") if ap.strip()
        ]

        self.model, self.known_bssids = joblib.load(model_path)

        self.esp32 = Esp32().connect_serial(serial_port, ignore)

        self.thread = threading.Thread(target=self.measure)
        self.thread.daemon = True
        self.thread.start()

    def measure(self):
        measurement = self.esp32.get_ap_rssis()

        # This doesn't seem like a good way to do it but oh well I didn't make the
        # AI code
        index_locked_measurement = [self.DEFAULT_RSSI] * len(self.known_bssids)
        for ap in measurement:
            try:
                index = self.known_bssids.index(ap["bssid"])
                index_locked_measurement[index] = ap["rssi"]
            except ValueError:
                continue

        self.x, self.y, *_ = self.model.predict([index_locked_measurement])[0]
