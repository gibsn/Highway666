import pygame
from pygame.locals import *


class GraphObject(pygame.sprite.Sprite):
    def __init__(self, topleft, image_path):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image_path).convert()

        self.rect = self.image.get_rect(topleft=topleft)

    def __init__(self, topleft, width, height, colour):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(colour))

        self.rect = self.image.get_rect(topleft=topleft)
