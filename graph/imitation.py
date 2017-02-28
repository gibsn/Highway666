import pygame
from pygame.locals import *

from model import road
from graph import moving_object


WIDTH = 640
HEIGHT = 320
DISPLAY = (WIDTH, HEIGHT)

FPS = 60
FPS_FONT_SIZE = 25
FPS_COLOUR = "#F5F53B"

BACKGROUND_COLOR = "#004400"


class Imitation:
    def __init__(self, speed_inf, speed_sup, spawn_inf, spawn_sup, slow_factor, slow_time):
        pygame.init()

        if not pygame.font:
            print('Warning, fonts disabled')
        if not pygame.mixer:
            print('Warning, sound disabled')

        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption("Highway666 by Kirill Alekseev")

        self.background = pygame.Surface(DISPLAY)
        self.background.fill(pygame.Color(BACKGROUND_COLOR))

        self.clock = pygame.time.Clock()

        self.road = road.Road(WIDTH, HEIGHT)
        self.environment = pygame.sprite.RenderUpdates(self.road)

#TODO get rid of this
        self.car = moving_object.MovingObject((0, 100), (100, 0), (1, 0), 10, 10, "blue")
        self.cars = pygame.sprite.RenderUpdates(self.car)

    def __handle_quit(self):
        print("Got 'quit' from pygame, stopping imitation")
        pygame.display.quit()

    def __show_fps(self):
        font = pygame.font.Font(None, FPS_FONT_SIZE)
        text = font.render("FPS: %.2f" % (self.clock.get_fps()), 1, pygame.Color(FPS_COLOUR))
        self.screen.blit(text, (0, 0))

        return text.get_rect()

    def __get_updates(self):
        updates = []
        time_passed = self.clock.get_time() / 1000.0

        self.environment.update()
        updates += self.environment.draw(self.screen)

        self.cars.update(time_passed)
        updates += self.cars.draw(self.screen)

        return updates

    def loop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.__handle_quit()
                    return

            self.screen.blit(self.background, (0, 0))

            updates = self.__get_updates()
            updates.append(self.__show_fps())

            pygame.display.update(updates)
