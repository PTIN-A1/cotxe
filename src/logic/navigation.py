import math

from peripherals.powertrain.powertrain import Powertrain


class Navigation:
    tolerance: float = 0.015

    angle: float = math.pi / 2.0
    angular_velocity: float = math.pi / 32  # rad / 500ms

    def calculate_direction(
        self, position: [float, float], destination: [float, float]
    ) -> Powertrain.Direction:
        distance = math.sqrt(
            (destination[0] - position[0]) ** 2 +
            (destination[1] - position[1]) ** 2
        )

        if distance <= self.tolerance:
            return Powertrain.Direction.Stop

        delta_x = destination[0] - position[0]
        delta_y = destination[1] - position[1]
        target_angle = math.atan2(delta_y, delta_x)

        target_angle = target_angle % (2 * math.pi)
        current_angle = self.angle % (2 * math.pi)

        angle_difference = (target_angle - current_angle + math.pi) % (
            2 * math.pi
        ) - math.pi

        if abs(angle_difference) < self.angular_velocity:
            return Powertrain.Direction.Forward

        if angle_difference > 0:
            return Powertrain.Direction.Left
        else:
            return Powertrain.Direction.Right
