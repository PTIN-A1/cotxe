import os

from peripherals.distance.distance import Distance
from peripherals.distance.ultrasonic import Ultrasonic
from peripherals.distance.virtual import VirtualDistance

ENVIRONMENT = os.getenv("ENVIRONMENT", "physical")


def to_subclass() -> Distance:
    if ENVIRONMENT == "physical":
        return Ultrasonic()
    else:
        return VirtualDistance()
