import pygame
from pygame.locals import *


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image_path):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image_path).convert()

        self.rect = self.image.get_rect()
        self.shape = (width, height)

    def __init__(self, width, height, colour):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(colour))

        self.rect = self.image.get_rect()
        self.shape = (width, height)


