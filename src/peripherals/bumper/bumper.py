from enum import Enum


class Side(Enum):
    front = "front"
    left = "left"
    right = "right"
    back = "back"
    false = "false"


class Bumper:
    collisioned: Side = Side.false
