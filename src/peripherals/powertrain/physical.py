from enum import Enum
import logging as log

from PCA9685_smbus2 import PCA9685

from peripherals.powertrain.powertrain import Powertrain, State


class PhysicalPowertrain(Powertrain):
    pwm: PCA9685

    class Motor(Enum):
        TopLeft = (0, 0, 1)
        TopRight = (1, 6, 7)
        BottomLeft = (2, 3, 2)
        BottomRight = (3, 4, 5)

    def powertain(self, interface: str):
        log.info(f"Connecting to powertrain on interface {interface}...")
        self.pwm = PCA9685.PCA9685(interface=interface)
        self.pwm.set_pwm_freq(50)
        log.info("Successfully connected to and configured the powertrain.")

    def set_motor(self, motor: Motor, direction: Powertrain.Direction):
        (index, channel_a, channel_b) = motor.value
        duty = direction.value[index]

        if duty > 0:
            self.pwm.set_pwm(channel_a, 0, 0)
            self.pwm.set_pwm(channel_b, 0, duty)

        elif duty < 0:
            self.pwm.set_pwm(channel_a, 0, abs(duty))
            self.pwm.set_pwm(channel_b, 0, 0)

        else:
            self.pwm.set_pwm(channel_a, 0, 4095)
            self.pwm.set_pwm(channel_b, 0, 4095)

    def move(self, direction: Powertrain.Direction):
        log.debug(f"Moving motors in direction {direction}")

        if direction == Powertrain.Direction.Stop:
            self.state = State.Stopped
        else:
            self.state = State.Moving

        self.set_motor(self.Motor.TopLeft, direction)
        self.set_motor(self.Motor.TopRight, direction)
        self.set_motor(self.Motor.BottomRight, direction)
        self.set_motor(self.Motor.BottomLeft, direction)
