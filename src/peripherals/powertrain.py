from enum import Enum


from PCA9685_smbus2 import PCA9685


class Powertrain:
    pwm: PCA9685

    class Direction(Enum):
        Forward = (2000, 2000, 2000, 2000)
        Back = (-2000, -2000, -2000, -2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)

    class Motor(Enum):
        TopLeft = (0, 0, 1)
        TopRight = (1, 6, 7)
        BottomLeft = (2, 3, 2)
        BottomRight = (3, 4, 5)

    def connect_powertain(self, interface: str):
        self.pwm = PCA9685.PCA9685(interface=interface)
        self.pwm.set_pwm_freq(50)

    def set_motor(self, motor: Motor, direction: Direction):
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

    def move(self, direction: Direction):
        self.set_motor(self.Motor.TopLeft, direction)
        self.set_motor(self.Motor.TopRight, direction)
        self.set_motor(self.Motor.BottomRight, direction)
        self.set_motor(self.Motor.BottomLeft, direction)
