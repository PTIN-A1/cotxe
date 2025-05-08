import os

from peripherals.distance.distance import Distance
from peripherals.distance.ultrasonic import Ultrasonic
from peripherals.distance.virtual import VirtualDistance

ENVIRONMENT = os.getenv("ENVIRONMENT", "physical")


def build_distance() -> Distance:
    if ENVIRONMENT == "physical":
        return Ultrasonic()
    else:
        return VirtualDistance()
