import time

from enum import Enum
import logging as log
from typing import Tuple

from peripherals.powertrain.powertrain import Powertrain
from peripherals.location.virtual import VirtualLocation


class VirtualPowertrain(Powertrain):
    def __init__(self, location: VirtualLocation):
        self.orientation = "north"
        self.location = location
        self.status = "Available"

    def connect_powertain(self, interface: str):
        log.info("Connecting to powertrain on virtual interface...")
        log.info("Successfully connected to and configured the powertrain.")

    # Avança cap al waypoint descrit a "destination", realitzant girs si és necessari per apuntar cap a on està el waypoint
    def move(self, destination):
        x_actual, y_actual = self.location.get()
        # destination típicament és una tupla de x i y que indica a quin waypoint ha d'arribar el vehicle
        if isinstance(destination, str):
            if destination == "Stop":
                self.change_status("Stopped")
        else:
            x_final, y_final = destination
            orientation_actual = self.get_orientation()
            log.info(f"El cotxe es troba a {x_actual}, {y_actual}")
            log.info(f"La destinació és {x_final}, {y_final}")

            # Mirem cap a on ha d'apuntar el cotxe segons l'ubicació actual i el waypoint de destí
            if y_final > y_actual:
                desired_orientation = "north"
            elif y_final < y_actual:
                desired_orientation = "south"
            elif x_final > x_actual:
                desired_orientation = "east"
            elif x_final < x_actual:
                desired_orientation = "west"
            else:
                desired_orientation = "Stop"

            # Girem fins aconseguir la direcció a la qual volem apuntar
            while True:
                orientation_actual = self.get_orientation()
                if orientation_actual == desired_orientation:
                    break
                # Els quatre casos per girar a la dreta:
                if (orientation_actual == "west" and desired_orientation == "north") or \
                   (orientation_actual == "north" and desired_orientation == "east") or \
                   (orientation_actual == "east" and desired_orientation == "south") or \
                   (orientation_actual == "south" and desired_orientation == "west"):
                    gir = ["north", "east", "south", "west"]
                    self.change_orientation(
                        gir[(gir.index(orientation_actual) + 1) % 4])
                else:
                    # Gir a l'esquerra
                    gir = ["north", "west", "south", "east"]
                    self.change_orientation(
                        gir[(gir.index(orientation_actual) + 1) % 4])
                # Emular temps de gir
                print(
                    f"Estic orientat a {orientation_actual} i vull orientar-me a {desired_orientation}")
                time.sleep(0.5)

            # El cotxe ja apunta cap a "desired_orientation", així que ja podem fer que avanci
            # Suposem que només hi ha diferència entre la x actual i la objectiu, o entre la y actual i la objectiu, però no a les dues coordenades a la vegada
            if y_actual == y_final:
                distance = abs(x_final - x_actual)
                # self.location.change_location("forward_x", distance)
            else:  # x_actual == x_final:
                distance = abs(y_final - y_actual)
                # self.location.change_location("forward_y", distance)
            self.location.change_location(x_final, y_final)
            x2, y2 = self.location.get()
            print(f"Estem ara a: {x2} {y2}")

    def get_orientation(self):
        return self.orientation

    def change_orientation(self, new_orientation):
        self.orientation = new_orientation
