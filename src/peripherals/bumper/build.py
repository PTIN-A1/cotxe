import os

from peripherals.bumper.bumper import Bumper
from peripherals.bumper.microswitches import Microswitches
from peripherals.bumper.virtual import VirtualBumper

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")


def build_bumper() -> Bumper:
    if ENVIRONMENT == "physical":
        return Microswitches()
    else:
        return VirtualBumper()
