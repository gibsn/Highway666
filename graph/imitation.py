import random
import os

import pygame
from pygame.locals import *

from model import road, car
from graph import static_object


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

        pygame.mixer.pre_init(frequency=44100, channels=8)
        pygame.init()

        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption("Highway666 by Kirill Alekseev")

        self.__loadCarSprites()
        self.__initGrass()

        self.__initSounds()

        self.clock = pygame.time.Clock()

        self.road = road.Road((0, HEIGHT/6.0), WIDTH, HEIGHT*2/3.0)
        self.environment = pygame.sprite.RenderUpdates(self.road)

        self.cars = pygame.sprite.RenderUpdates()
        self.__spawnCarHandler()

    def __initGrass(self):
        image = pygame.image.load("sprites/Tiles/Grass/land_grass04.png").convert()
        tile_width, tile_height = image.get_size()

        self.grass = pygame.sprite.RenderUpdates()

        for i in xrange(WIDTH/tile_width + 1):
            for j in xrange(HEIGHT/tile_height + 1):
                topleft = (i * tile_width, j * tile_height)
                self.grass.add(static_object.StaticObject(topleft, image=image))

    def __loadCarSprites(self):
        colours = ["black", "blue", "green", "red", "yellow"]
        nums = ["1", "2", "3", "4", "5"]
        prefix = "sprites/Cars/car_"
        paths = [os.path.join(prefix+c+"_"+n+".png") for c in colours for n in nums]

        self.car_images = [pygame.image.load(path).convert_alpha() for path in paths]
        self.car_images = list(map(lambda a: pygame.transform.rotate(a, -90), self.car_images))

    def __initSounds(self):
        self.explosion_sound = pygame.mixer.Sound(file="sounds/explosion.ogg")
        self.birds_sound = pygame.mixer.Sound(file="sounds/birds.ogg")
        self.car_sounds = [pygame.mixer.Sound(file="sounds/car_"+n+".ogg") for n in ["1", "2", "3"]]

        self.birds_sound.play(loops=-1)

    def __spawnCarHandler(self):
        newCar = self.road.spawnCar(self.speed_inf, self.speed_sup, random.choice(self.car_images))
        self.cars.add(newCar)

        newCar.sound = random.choice(self.car_sounds)
        newCar.sound.play(loops=-1)

        time_to_next_spawn = random.randint(self.spawn_inf*1000, self.spawn_sup*1000)
        pygame.time.set_timer(SPAWN_CAR_EVENT, time_to_next_spawn)

    def __quitHandler(self):
        print("Got 'quit' from pygame, stopping imitation")
        pygame.quit()

    def __showFps(self):
        font = pygame.font.Font(None, FPS_FONT_SIZE)
        text = font.render("FPS: %.2f" % (self.clock.get_fps()), 1, pygame.Color(FPS_COLOUR))
        self.screen.blit(text, (0, 0))

        return text.get_rect()

    def __getUpdates(self):
        updates = []
        time_passed = self.clock.get_time() / 1000.0

        updates += self.grass.draw(self.screen)

        self.environment.update()
        updates += self.environment.draw(self.screen)

        self.cars.update(time_passed)
        updates += self.cars.draw(self.screen)

        return updates

    def __checkCrashes(self):
        collisions = pygame.sprite.groupcollide(self.cars, self.cars, False, False)

        for k, v in collisions.iteritems():
            for car in v:
                if k != car:
                    k.crash(), car.crash()
                    self.explosion_sound.play()

    def __removeGoneCars(self):
        for c in self.cars:
            x, y = c.rect.topleft
            if x > WIDTH or y > HEIGHT:
                c.kill()

    def loop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.__quitHandler()
                    return
                elif event.type == SPAWN_CAR_EVENT:
                    self.__spawnCarHandler()

            self.__checkCrashes()
            self.__removeGoneCars()

            updates = self.__getUpdates()
            updates.append(self.__showFps())

            pygame.display.update(updates)
