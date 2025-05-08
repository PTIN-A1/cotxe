import os

from peripherals.location.location import Location
from peripherals.location.virtual import VirtualLocation
from peripherals.location.physical import PhysicalLocation

ENVIRONMENT = os.getenv("ENVIRONMENT", "physical")


def build_location() -> Location:
    if ENVIRONMENT == "physical":
        return PhysicalLocation()
    else:
        return VirtualLocation()
