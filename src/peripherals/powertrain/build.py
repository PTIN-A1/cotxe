import os

from peripherals.powertrain.powertrain import Powertrain
from peripherals.powertrain.physical import PhysicalPowertrain
from peripherals.powertrain.virtual import VirtualPowertrain

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")
INTERFACE = os.getenv("POWERTRAIN", "/dev/i2c-2")


def build_powertrain() -> Powertrain:
    if ENVIRONMENT == "physical":
        powertrain = PhysicalPowertrain()
        powertrain.connect(INTERFACE)
        return powertrain
    else:
        return VirtualPowertrain()
