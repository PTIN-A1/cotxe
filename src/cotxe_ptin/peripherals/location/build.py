import os

from .location import Location
from .virtual import VirtualLocation
from .physical import PhysicalLocation

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")


def build_location() -> Location:
    if ENVIRONMENT == "physical":
        return PhysicalLocation()
    else:
        return VirtualLocation()
