from enum import Enum


class State(Enum):
    Stopped = "stopped"
    Moving = "moving"


class Powertrain:
    state: State = State.Stopped

    class Direction(Enum):
        Forward = (-2000, -2000, -2000, -2000)
        Back = (2000, 2000, 2000, 2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)
