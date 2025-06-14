import threading
import time


from peripherals.bumper.bumper import Bumper, Side


class Microswitches(Bumper):
    def __init__(self):
        self.thread = threading.Thread(target=self.read_switches)
        self.thread.daemon = True
        self.thread.start()

        from gpiozero import Button
        self.front = Button(21)
        self.back = Button(20)
        self.left = Button(16)
        self.right = Button(12)

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
