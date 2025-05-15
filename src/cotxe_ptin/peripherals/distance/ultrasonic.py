import warnings
import time

from gpiozero import DistanceSensor, PWMSoftwareFallback, DistanceSensorNoEcho

from .distance import Distance


class Ultrasonic(Distance):
    def __init__(
        self, trigger_pin: int = 154, echo_pin: int = 156, max_distance: float = 3.0
    ):
        warnings.filterwarnings("ignore", category=DistanceSensorNoEcho)
        warnings.filterwarnings("ignore", category=PWMSoftwareFallback)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.max_distance = max_distance
        self.sensor = DistanceSensor(
            echo=self.echo_pin, trigger=self.trigger_pin, max_distance=self.max_distance
        )

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def measure(self) -> float:
        try:
            distance = self.sensor.distance * 100
            time.sleep(0.5)
            return round(float(distance), 1)
        except RuntimeWarning as e:
            print(f"Warning: {e}")
            return None

    def close(self):
        self.sensor.close()
