import os

from peripherals.powertrain.powertrain import Powertrain
from peripherals.powertrain.physical import PhysicalPowertrain
from peripherals.powertrain.virtual import VirtualPowertrain

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")


def build_powertrain() -> Powertrain:
    if ENVIRONMENT == "physical":
        return PhysicalPowertrain()
    else:
        return VirtualPowertrain()
