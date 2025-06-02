import threading
import time

from gpiozero import Button

from peripherals.bumper.bumper import Bumper, Side


class Microswitches(Bumper):
    front = Button(21)
    back = Button(20)
    left = Button(16)
    right = Button(12)

    def __init__(self):
        self.thread = threading.Thread(target=self.read_switches)
        self.thread.daemon = True
        self.thread.start()

    def read_switches(self):
        while True:
            if self.front.is_pressed:
                self.collision(Side.front)

            if self.back.is_pressed:
                self.collision(Side.back)

            if self.left.is_pressed:
                self.collision(Side.left)

            if self.right.is_pressed:
                self.collision(Side.right)

    def collision(self, side: Side):
        self.collisioned = side
        time.sleep(0.25)
