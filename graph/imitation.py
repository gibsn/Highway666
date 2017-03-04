import random
import os

import pygame
from pygame.locals import *

from model import road, car


WIDTH = 640
HEIGHT = 320
DISPLAY = (WIDTH, HEIGHT)

FPS = 60
FPS_FONT_SIZE = 25
FPS_COLOUR = "#F5F53B"

BACKGROUND_COLOR = "#004400"

SPAWN_CAR_EVENT = pygame.USEREVENT + 1

MS = 1000


class Imitation:
    def __init__(self, speed_inf, speed_sup, spawn_inf, spawn_sup, slow_factor, slow_time):
        self.speed_inf, self.speed_sup = speed_inf, speed_sup
        self.spawn_inf, self.spawn_sup = spawn_inf, spawn_sup
        self.slow_factor, self.slow_time = slow_factor, slow_time

        pygame.init()

        if not pygame.font:
            print('Warning, fonts disabled')
        if not pygame.mixer:
            print('Warning, sound disabled')

        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption("Highway666 by Kirill Alekseev")

        self.background = pygame.Surface(DISPLAY)
        self.background.fill(pygame.Color(BACKGROUND_COLOR))

        self.__loadSprites()

        self.clock = pygame.time.Clock()

        self.road = road.Road((0, HEIGHT/6.0), WIDTH, HEIGHT*2/3.0)
        self.environment = pygame.sprite.RenderUpdates(self.road)

        self.cars = pygame.sprite.RenderUpdates()
        self.cars.add(self.road.spawnCar(speed_inf, speed_sup, random.choice(self.car_images)))

        time_to_next_spawn = random.randint(self.spawn_inf*1000, self.spawn_sup*1000)
        pygame.time.set_timer(SPAWN_CAR_EVENT, time_to_next_spawn)

    def __loadSprites(self):
        colours = ["black", "blue", "green", "red", "yellow"]
        nums = ["1", "2", "3", "4", "5"]
        path = "sprites/Cars/car_"
        paths = [os.path.join(path+c+"_"+n+".png") for c in colours for n in nums]

        self.car_images = [pygame.image.load(path).convert_alpha() for path in paths]
        self.car_images = list(map(lambda a: pygame.transform.rotate(a, -90), self.car_images))

    def __handleQuit(self):
        print("Got 'quit' from pygame, stopping imitation")
        pygame.display.quit()

    def __showFps(self):
        font = pygame.font.Font(None, FPS_FONT_SIZE)
        text = font.render("FPS: %.2f" % (self.clock.get_fps()), 1, pygame.Color(FPS_COLOUR))
        self.screen.blit(text, (0, 0))

        return text.get_rect()

    def __getUpdates(self):
        updates = []
        time_passed = self.clock.get_time() / 1000.0

        self.environment.update()
        updates += self.environment.draw(self.screen)

        self.cars.update(time_passed)
        updates += self.cars.draw(self.screen)

        return updates

    def __removeGoneCars(self):
        for car in self.cars:
            x, y = car.rect.topleft
            if x > WIDTH or y > HEIGHT:
                car.kill()

    def loop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.__handleQuit()
                    return
                elif event.type == SPAWN_CAR_EVENT:
                    image = random.choice(self.car_images)
                    self.cars.add(self.road.spawnCar(self.speed_inf, self.speed_sup, image))

                    time_to_next_spawn = random.randint(self.spawn_inf*MS, self.spawn_sup*MS)
                    pygame.time.set_timer(SPAWN_CAR_EVENT, time_to_next_spawn)

            self.__removeGoneCars()

            self.screen.blit(self.background, (0, 0))

            updates = self.__getUpdates()
            updates.append(self.__showFps())

            pygame.display.update(updates)
