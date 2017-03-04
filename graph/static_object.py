# import pygame
# from pygame.locals import *

from graph import graph_object


class StaticObject(graph_object.GraphObject):
    def __init__(self, topleft, width, height, colour="blue", image=None):
        if image:
            graph_object.GraphObject.__init__(self, topleft, image)
        else:
            graph_object.GraphObject.__init__(self, topleft, width, height, colour)
