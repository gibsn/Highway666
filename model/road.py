import random

from graph import static_object
from model import car


class Road(static_object.StaticObject):
    def __init__(self, topleft, width, height, image=None):
            static_object.StaticObject.__init__(self, topleft, width, height, "grey", image)

            self.topleft = topleft
            self.shape = (width, height)

    def spawnCar(self, min_speed, max_speed, image):
        speed = (random.randint(min_speed, max_speed)*2, 0)
        width, height = image.get_size()
        car_topleft = -width, self.topleft[1] + self.shape[1]/2 - height/2

        return car.Car(car_topleft, speed, width, height, image)
