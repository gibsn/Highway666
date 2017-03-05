import numpy as np

from graph import moving_object


class CarState():
    OK = 0
    CRASHED = 1
    SLOWING_DOWN = 2
    SPEEDING_UP = 3


class Car(moving_object.MovingObject):
    def __init__(self, topleft, speed, width=0, height=0, image=None):
        moving_object.MovingObject.__init__(self, topleft, speed, (0, 0), width, height, image=image)

        self.initial_speed = np.array(speed, np.float64) * moving_object.MAGIC
        self.state = CarState.OK

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def kill(self):
        super(Car, self).kill()
        self.sound.fadeout(1000)

    def crash(self):
        self.sound.stop()

        self.speed = np.array((0, 0), np.float64)
        self.acceleration = np.array((0, 0), np.float64)

        self.state = CarState.CRASHED

    def slowDown(self, wanted_speed):
        if self.state == CarState.OK:
            self.state = CarState.SLOWING_DOWN
            self.acceleration = np.array((-100, 0), np.float64)
            self.wanted_speed = np.array(wanted_speed, np.float64)

    def speedUp(self):
        if self.state == CarState.OK:
            self.state = CarState.SPEEDING_UP
            self.acceleration = np.array((100, 0), np.float64)
            self.wanted_speed = self.initial_speed

    def update(self, *args):
        super(Car, self).update(*args)

        if self.state == CarState.SLOWING_DOWN:
            if np.linalg.norm(self.speed) <= np.linalg.norm(self.wanted_speed):
                self.state = CarState.OK
                self.acceleration = np.array((0, 0), np.float64)
        elif self.state == CarState.SPEEDING_UP:
            if np.linalg.norm(self.speed) >= np.linalg.norm(self.wanted_speed):
                self.state = CarState.OK
                self.acceleration = np.array((0, 0), np.float64)
