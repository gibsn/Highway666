import random
import os
import Queue

import pygame
from pygame.locals import *

from model import road, car
from model.car import CarState
from graph import static_object


WIDTH = 1280
HEIGHT = 300
DISPLAY = (WIDTH, HEIGHT)

FPS = 30
FPS_FONT_SIZE = 25
FPS_COLOUR = "#F5F53B"

SPAWN_CAR_EVENT = pygame.USEREVENT + 1
KILL_CRASHED_CAR_EVENT = pygame.USEREVENT + 2
SPEED_UP_TIMER_EVENT = pygame.USEREVENT + 3

SEC = 1000

KILL_CRASHED_CAR_TIME = 1 * SEC


class Imitation:
    def __init__(self, speed_inf, speed_sup, spawn_inf, spawn_sup, slow_factor, slow_time):
        self.speed_inf, self.speed_sup = speed_inf, speed_sup
        self.spawn_inf, self.spawn_sup = spawn_inf, spawn_sup
        self.slow_factor, self.slow_time = slow_factor, slow_time

        pygame.mixer.pre_init(frequency=44100, channels=8)
        pygame.init()

        self.clock = pygame.time.Clock()

        self.__initDisplay()
        self.__initSounds()
        self.__initGrass()
        self.__initRoad()
        self.__initCars()

    def __initRoad(self):
        k = 3
        self.road = road.Road((0, HEIGHT*(k/2)/k), WIDTH, HEIGHT/k)
        self.environment = pygame.sprite.RenderUpdates(self.road)

    def __initCars(self):
        self.__loadCarSprites()

        self.cars = pygame.sprite.RenderUpdates()
        self.__spawnCarHandler()
        self.crashed_cars = Queue.Queue()
        self.curr_slow_car = None

    def __initDisplay(self):
        flags = 0
        # flags = pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(DISPLAY, flags)
        pygame.display.set_caption("Highway666 by Kirill Alekseev")

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
        self.brakes_sound = pygame.mixer.Sound(file="sounds/brakes.ogg")
        self.birds_sound = pygame.mixer.Sound(file="sounds/birds.ogg")
        self.car_sounds = [pygame.mixer.Sound(file="sounds/car_"+n+".ogg") for n in ["1", "2", "3"]]

        self.birds_sound.play(loops=-1)

    def __showFps(self):
        font = pygame.font.Font(None, FPS_FONT_SIZE)
        text = font.render("FPS: %.2f" % (self.clock.get_fps()), 1, pygame.Color(FPS_COLOUR))
        # print("FPS: %.2f" % (self.clock.get_fps()))
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

    def __checkCrash(self, rear_car, front_car):
        crash = False
        def __crash(c):
            c.sound.stop()
            c.crash()
            self.crashed_cars.put(c)

        if pygame.sprite.collide_rect(rear_car, front_car):
            if front_car.state != CarState.CRASHED:
                __crash(front_car)
                crash = True

            if rear_car.state != CarState.CRASHED:
                __crash(rear_car)
                crash = True

            if crash:
                pygame.time.set_timer(KILL_CRASHED_CAR_EVENT, KILL_CRASHED_CAR_TIME)
                self.explosion_sound.play()

    def __maybeSlowDown(self, rear_car, front_car):
        if pygame.sprite.collide_rect_ratio(3.0)(rear_car, front_car):
            if rear_car.state == CarState.OK:
                rear_car.slowDown(front_car.speed)
                rear_car.front_car = front_car

                self.brakes_sound.play()

    def __carsHandler(self):
        for car_1 in self.cars:
            for car_2 in self.cars:
                if car_1 != car_2:
                    rear_car = car_1 if car_1.rect.topleft < car_2.rect.topleft else car_2
                    front_car = car_1 if rear_car != car_1 else car_2

                    self.__checkCrash(rear_car, front_car)
                    self.__maybeSlowDown(rear_car, front_car)

            car_1.maybeSpeedUp()
            self.__removeGoneCar(car_1)

    def __removeGoneCar(self, c):
        x, y = c.rect.topleft
        if x > WIDTH or y > HEIGHT:
            c.kill()

    def __quitHandler(self):
        print("Got 'quit' from pygame, stopping imitation")
        pygame.quit()

    def __spawnCarHandler(self):
        newCar = self.road.spawnCar(self.speed_inf, self.speed_sup, random.choice(self.car_images))
        self.cars.add(newCar)

        newCar.sound = random.choice(self.car_sounds)
        newCar.sound.play(loops=-1)

        time_to_next_spawn = random.randint(self.spawn_inf*SEC, self.spawn_sup*SEC)
        pygame.time.set_timer(SPAWN_CAR_EVENT, time_to_next_spawn)

    def __killCrashedCarHandler(self):
        if not self.crashed_cars.empty():
            self.crashed_cars.get().kill()
        else:
            pygame.time.set_timer(KILL_CRASHED_CAR_EVENT, 0)

    def __slowingHandler(self, event):
        if self.curr_slow_car:
            print("Only one manual slowing down is permitted")
            return

        if event.button == 1:
            for c in self.cars:
                if c.collidepoint(event.pos):
                    c.manuallySlowDown(self.slow_factor * c.initial_speed)
                    self.curr_slow_car = c
                    pygame.time.set_timer(SPEED_UP_TIMER_EVENT, self.slow_time * SEC)

                    self.brakes_sound.play()
                    return

    def __speedUpHandler(self):
        pygame.time.set_timer(SPEED_UP_TIMER_EVENT, 0)
        if self.curr_slow_car.state != CarState.CRASHED:
            self.curr_slow_car.speedUp()
        self.curr_slow_car = None

    def __handler(self, event):
        def default(): pass

        if event.type == pygame.QUIT or\
           event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return self.__quitHandler
        elif event.type == SPAWN_CAR_EVENT:
            return self.__spawnCarHandler
        elif event.type == KILL_CRASHED_CAR_EVENT:
            return self.__killCrashedCarHandler
        elif event.type == SPEED_UP_TIMER_EVENT:
            return self.__speedUpHandler
        elif event.type == MOUSEBUTTONDOWN:
            return lambda: self.__slowingHandler(event)
        else:
            return default

    def loop(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.__handler(event)()

            self.__carsHandler()

            updates = self.__getUpdates()
            updates.append(self.__showFps())

            pygame.display.update(updates)
