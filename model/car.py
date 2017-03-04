import numpy as np

from graph import moving_object


class Car(moving_object.MovingObject):
    def __init__(self, topleft, speed, width=0, height=0, image=None):
        moving_object.MovingObject.__init__(self, topleft, speed, (0, 0), width, height, image=image)

        self.wanted_speed = speed

    def kill(self):
        super(Car, self).kill()
        self.sound.fadeout(1000)

    def crash(self):
        self.sound.stop()

        self.speed = np.array([0, 0], np.float64)
        self.acceleration = np.array([0, 0], np.float64)
