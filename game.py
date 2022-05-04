import math
import random

import pygame as pg
from controller import Controller


class GameObject:
    def __init__(self, name: str, sizes: tuple, gravity, gnd: float, base_speed: tuple):
        self.name = name
        self.bounding_box = pg.rect.Rect(0, 0, sizes[0], sizes[1])
        self.hitbox = self.setHitbox()
        self.dx = 0.0
        self.dy = 0.0
        self.gravity = gravity
        self.gnd = gnd
        self.base_speed = base_speed
        self.on_ground = True
        self.alive = True

    def tick(self, obstacles: list = None, game_state: dict = None):
        # should do physics and call update
        self.bounding_box.move_ip(self.dx, self.dy)
        self.update(obstacles, game_state)

    def update(self, obstacles: list = None, game_state: dict = None):
        # virtual
        return

    def setHitbox(self) -> pg.Rect:
        return self.bounding_box

    def moveTo(self, x, y):
        self.bounding_box.left, self.bounding_box.bottom = x, y

    def setSpeed(self, dx, dy):
        self.dx = dx + self.base_speed[0]
        self.dy = dy + self.base_speed[1]


class Dino(GameObject):
    def control(self, controls: Controller, jump_speed):
        # jump and duck
        if controls['jump'] and self.on_ground:
            self.dy = jump_speed

    def update(self, obstacles: list = None, game_state: dict = None):
        # jump physics
        if self.on_ground and self.dy < 0:
            self.on_ground = False
        else:
            self.dy += self.gravity
            if self.bounding_box.bottom >= self.gnd:
                self.moveTo(self.bounding_box.left, self.gnd)
                self.dy = 0
                self.on_ground = True

        # collisions
        for obst in obstacles:
            if self.hitbox.colliderect(obst.hitbox):
                self.alive = False


class AbstractDinoGame:
    """
    An abstract version of the dino game, implementable in different configurations.
    """

    def __init__(self, controls: Controller, display_rect: tuple, image_sizes: dict, frame_delay: int, scale: float):
        # game controller and bounding rect
        self.ctrl = controls
        self.game_display = pg.rect.Rect(display_rect)
        self.image_sizes = image_sizes

        # game constants
        self.frames = 0
        self.spawn_wait = 0
        self.sf = scale
        self.fd = frame_delay
        self.gnd = self.game_display.h * 0.9

        # kinematics constants
        self.init_velocity = 20 * self.sf * (self.fd / 30)
        self.dino_jump_velocity = -38 * self.sf * (self.fd / 30)
        self.gravity = 3.5 * self.sf * ((self.fd / 30)**2)
        self.dino_accel_rate = 0.1 * self.sf * (self.fd / 30)
        self.speed_increase_tick = int(15 * (30 / self.fd))
        self.spawn_const = int(25 * (30 / self.fd))

        # dino
        self.dino = self.initDino()

        # obstacles (6 cacti and 2 pterodactyls)
        self.obstacles = self.initObstacles()
        self.obstacles_in_play = []

        # overall game state variables
        self.state = {
            'playing': False,
            'freeze': False,
            'showhb': False,
            'score': 0,
            'ground_level': self.gnd,
            'game_speed': self.init_velocity,
            'on_ground': True,
            'dino': self.dino,
            'obstacles': self.obstacles_in_play
        }

    def tick(self):
        if self.state['playing']:
            # run game loop here

            # Increase the speed to the max
            if self.frames % self.speed_increase_tick == 0 and self.state['game_speed'] < 40:
                self.state['game_speed'] += self.dino_accel_rate
            if self.state['game_speed'] >= 40:
                print('max speed')

            # control the dino
            self.dino.control(self.ctrl, self.dino_jump_velocity)

            # Tick the dino and all the obstacles
            self.dino.tick(obstacles=self.obstacles_in_play)
            self.state['on_ground'] = self.dino.on_ground
            for obstacle in self.obstacles_in_play:
                obstacle.tick()
                obstacle.setSpeed(-1 * self.state['game_speed'], 0)
                if obstacle.hitbox.right < 0:
                    self.state['score'] += 1
                    obstacle.moveTo(0, obstacle.hitbox.h)
                    obstacle.setSpeed(0, 0)
                    self.obstacles_in_play.remove(obstacle)

            if self.dino.alive is False:
                self.state['playing'] = False

            # call update for controls
            self.update()

            # Spawn new Obstacles
            self.spawnObstacle()

            self.state['obstacles'] = self.obstacles_in_play
            self.spawn_wait += 1

            self.frames += 1
            # self.state['score'] = int(self.frames * (self.fd / 30))

        else:
            if self.ctrl['play']:
                self.frames = 0
                self.reset()
                self.state['playing'] = True

    def update(self):
        return

    def spawnObstacle(self):
        if random.randint(1, self.spawn_const) == 1:
            index = random.randint(0, len(self.obstacles) - 1) #index =  #random.randint(0, len(self.obstacles) - 1)

            chosen_obst = self.obstacles[index]
            min_wait = self.spawn_const #+ (2 * math.log(self.state['game_speed'] + 1))
            if chosen_obst.name == 'ptero':
                min_wait *= 1.5
            if self.spawn_wait > min_wait and chosen_obst not in self.obstacles_in_play:
                self.spawn_wait = 0
                if chosen_obst.name == 'ptero':
                    height = self.gnd - (self.dino.hitbox.h * random.randint(0, 2))
                    chosen_obst.moveTo(self.game_display.w, height)
                else:
                    chosen_obst.moveTo(self.game_display.w, self.gnd)
                self.obstacles_in_play.append(chosen_obst)

    def reset(self):
        self.dino.alive = True
        self.dino.moveTo(self.game_display.w * 0.1, self.gnd)
        self.obstacles_in_play = []
        self.state['playing'] = False
        self.state['score'] = 0
        self.state['game_speed'] = self.init_velocity
        self.state['on_ground'] = True

    def initDino(self) -> Dino:
        dino = Dino('dino', self.image_sizes['dino'], self.gravity, self.gnd, (0, 0))
        dino.moveTo(self.game_display.w * 0.1, self.gnd)
        return dino

    def initObstacles(self):
        # initialize the obstacles by scaling their raw image sizes
        obstacles = []
        for name, size in self.image_sizes.items():
            if name != 'dino':
                if name == 'ptero':
                    spd = -5 * self.sf * (self.fd / 30)
                else:
                    spd = 0
                obst = GameObject(name, size, 0, self.gnd, (spd, 0))
                obstacles.append(obst)
        return obstacles

    def getBounds(self):
        return self.dino.bounding_box, self.obstacles_in_play

    def getGameState(self):
        return self.state
