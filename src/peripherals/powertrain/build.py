import os

from peripherals.powertrain.powertrain import Powertrain
from peripherals.powertrain.physical import PhysicalPowertrain
from peripherals.powertrain.virtual import VirtualPowertrain

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")
<<<<<<< HEAD
=======
INTERFACE = os.getenv("POWERTRAIN", "/dev/i2c-1")
>>>>>>> a713f028ad786e48361dc06b97ac86277a6993d3


def build_powertrain() -> Powertrain:
    if ENVIRONMENT == "physical":
<<<<<<< HEAD
        return PhysicalPowertrain()
=======
        powertrain = PhysicalPowertrain()
        powertrain.connect(INTERFACE)
        return powertrain
>>>>>>> a713f028ad786e48361dc06b97ac86277a6993d3
    else:
        return VirtualPowertrain()
