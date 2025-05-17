import threading
import time
from math import sin, cos

from peripherals.powertrain.powertrain import Powertrain, State
from peripherals.location.location import Location
from logic.navigation import Navigation


class VirtualPowertrain(Powertrain):
    direction: Powertrain.Direction = Powertrain.Direction.Stop
    angle: float = 0
    speed: float = 0.01

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
                Navigation.angle += Navigation.angular_velocity
            case Powertrain.Direction.Right:
                Navigation.angle += -Navigation.angular_velocity

        time.sleep(0.5)

    def move(self, direction: Powertrain.Direction):
        if direction == Powertrain.Direction.Stop:
            self.state = State.Stopped
        else:
            self.state = State.Moving

        self.direction = direction
