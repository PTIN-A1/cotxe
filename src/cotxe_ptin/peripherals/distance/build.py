import os

from .distance import Distance
from .ultrasonic import Ultrasonic
from .virtual import VirtualDistance

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")


def build_distance() -> Distance:
    if ENVIRONMENT == "physical":
        return Ultrasonic()
    else:
        return VirtualDistance()
