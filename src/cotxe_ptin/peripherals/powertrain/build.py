import os

from .powertrain import Powertrain
from .physical import PhysicalPowertrain
from .virtual import VirtualPowertrain

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")


def build_powertrain(location) -> Powertrain:
    if ENVIRONMENT == "physical":
        return PhysicalPowertrain
    else:
        return VirtualPowertrain(location)
