import pygame
from pygame.locals import *


class GraphObject(pygame.sprite.Sprite):
    def __init__(self, topleft, width, height, colour, image=None):
        pygame.sprite.Sprite.__init__(self)

        if image:
            self.image = image
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(pygame.Color(colour))

        self.rect = self.image.get_rect(topleft=topleft)
