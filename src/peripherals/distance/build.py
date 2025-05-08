import os

from distance import Distance
from ultrasonic import Ultrasonic
from virtual import VirtualDistance

ENVIRONMENT = os.getenv("ENVIRONMENT", "physical")


def to_subclass() -> Distance:
    if ENVIRONMENT == "physical":
        return Ultrasonic()
    else:
        return VirtualDistance()
