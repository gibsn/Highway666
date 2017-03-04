# import pygame
# from pygame.locals import *

from graph import graph_object


class StaticObject(graph_object.GraphObject):
    def __init__(self, topleft, width=0, height=0, colour="blue", image=None):
        graph_object.GraphObject.__init__(self, topleft, width, height, colour, image)
