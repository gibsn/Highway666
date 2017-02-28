# import pygame
# from pygame.locals import *

from graph import graph_object


class StaticObject(graph_object.GraphObject):
    def __init__(self, topleft, image_path):
        graph_object.GraphObject.__init__(self, topleft, image_path)

    def __init__(self, topleft, width, height, colour):
        graph_object.GraphObject.__init__(self, topleft, width, height, colour)
