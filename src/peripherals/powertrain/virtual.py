import threading
import time
from math import sin, cos

from peripherals.powertrain.powertrain import Powertrain
from peripherals.location.location import Location


class VirtualPowertrain(Powertrain):
    direction: Powertrain.Direction = Powertrain.Direction.Stop
    angle: float = 0
    speed: float = 0.01
    angular_velocity: float = 0.314

    def __init__(self):
        self.thread = threading.Thread(target=self.update_location)

    def update_location(self):
        match self.direction:
            case Powertrain.Direction.Stop:
                pass
            case Powertrain.Direction.Forward:
                Location().x += cos(self.angle) * self.speed
                Location().y += sin(self.angle) * self.speed
            case Powertrain.Direction.Back:
                Location().x += cos(self.angle) * -self.speed
                Location().y += sin(self.angle) * -self.speed
            case Powertrain.Direction.Left:
                self.angle += self.angular_velocity
            case Powertrain.Direction.Right:
                self.angle += -self.angular_velocity

        time.sleep(0.5)

    def move(self, direction: Powertrain.Direction):
        self.direction = direction
