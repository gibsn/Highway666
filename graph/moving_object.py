import numpy as np

import pygame
from pygame.locals import *

from graph import graph_object


MAGIC = 3


class MovingObject(graph_object.GraphObject):
    def __init__(self, topleft, speed, acc,
                 width=0, height=0, colour="blue",
                 image=None):
        if image:
            graph_object.GraphObject.__init__(self, topleft, image)
        else:
            graph_object.GraphObject.__init__(self, topleft, width, height, colour)

        self.speed = np.array(speed, np.float64) * MAGIC
        self.acceleration = np.array(acc, np.float64) * MAGIC

    def update(self, time_passed):
        distance_change = self.speed * time_passed + self.acceleration * time_passed * time_passed / 2

        self.rect.move_ip(*distance_change)
        self.speed += self.acceleration * time_passed
