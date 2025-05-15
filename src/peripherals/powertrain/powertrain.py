from enum import Enum


class Powertrain():
    def __init__(self):
        self.status = "Available"

    class Direction(Enum):
        Forward = (-2000, -2000, -2000, -2000)
        Back = (2000, 2000, 2000, 2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)

    def get_status(self):
        return self.status

    def change_status(self, new_status):
        self.status = new_status
