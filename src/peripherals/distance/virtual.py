import random

from peripherals.distance.distance import Distance


class VirtualDistance(Distance):
    def measure(self) -> float:
        distance = round(random.uniform(35, 50), 1)
        return round(float(distance), 1)
