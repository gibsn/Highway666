import pygame
from pygame.locals import *


WIDTH = 640
HEIGHT = 320
DISPLAY = (WIDTH, HEIGHT)

FPS = 60

BACKGROUND_COLOR = "#004400"


class Imitation:
    def __init__(self, speed_inf, speed_sup, spawn_inf, spawn_sup, slow_factor, slow_time):
        pygame.init()

        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption("Highway666 by Kirill Alekseev")

        self.background = pygame.Surface(DISPLAY)
        self.background.fill(pygame.Color(BACKGROUND_COLOR))

        self.clock = pygame.time.Clock()

    def handle_quit(self):
        print("Got 'quit' from pygame, stopping imitation")
        pygame.display.quit()

    def loop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.handle_quit()
                    return

            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
