import numpy as np
import pygame

from graph import moving_object


class CarState():
    OK = 0
    CRASHED = 1
    SLOWING_DOWN = 2
    MOVING_SLOW = 3
    MANUALLY_SLOWING_DOWN = 4
    MANUALLY_MOVING_SLOW = 5
    SPEEDING_UP = 6


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
        self.speed = np.array((0, 0), np.float64)
        self.acceleration = np.array((0, 0), np.float64)

        self.state = CarState.CRASHED

    def maybeSpeedUp(self):
        if self.state == CarState.MOVING_SLOW or\
           self.state == CarState.SLOWING_DOWN:
            if self.front_car:
                if not pygame.sprite.collide_rect_ratio(3.0)(self, self.front_car):
                    self.speedUp()
                    self.front_car = None

    def __slowDown(self, wanted_speed):
        self.acceleration = np.array((-50, 0), np.float64)
        self.wanted_speed = np.array(wanted_speed, np.float64)

    def slowDown(self, wanted_speed):
        self.state = CarState.SLOWING_DOWN
        self.__slowDown(wanted_speed)

    def manuallySlowDown(self, wanted_speed):
        self.state = CarState.MANUALLY_SLOWING_DOWN
        self.__slowDown(wanted_speed)

    def speedUp(self):
        print(self.state)
        self.state = CarState.SPEEDING_UP
        self.acceleration = np.array((50, 0), np.float64)
        self.wanted_speed = self.initial_speed

    def update(self, *args):
        super(Car, self).update(*args)

        if self.state == CarState.SLOWING_DOWN:
            if np.linalg.norm(self.speed) <= np.linalg.norm(self.wanted_speed):
                self.state = CarState.MOVING_SLOW
                self.acceleration = np.array((0, 0), np.float64)
        if self.state == CarState.MANUALLY_SLOWING_DOWN:
            if np.linalg.norm(self.speed) <= np.linalg.norm(self.wanted_speed):
                self.state = CarState.MANUALLY_MOVING_SLOW
                self.acceleration = np.array((0, 0), np.float64)
        elif self.state == CarState.SPEEDING_UP:
            if np.linalg.norm(self.speed) >= np.linalg.norm(self.wanted_speed):
                self.state = CarState.OK
                self.acceleration = np.array((0, 0), np.float64)
