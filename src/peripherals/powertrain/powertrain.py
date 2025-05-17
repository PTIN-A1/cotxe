from enum import Enum


class Powertrain:
    class Direction(Enum):
        Forward = (-2000, -2000, -2000, -2000)
        Back = (2000, 2000, 2000, 2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)
