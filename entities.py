import time

import pygame

import debugger
from settings import *


# represents the user player
class Player(pygame.sprite.Sprite):
    # creates a player in the given position and set atrributes
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(64,64))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = SPEED
        self.jump_speed = -16
        self.in_air = True
        self.gravity = 0.8

    # Updates player
    def update(self):
        self.input()


    # Moves player
    def move(self):
        self.rect.x += self.direction.x * self.speed
        debugger.debug(self.direction * self.speed)

    # Applies gravity to player
    def apply_grav(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Sets direction according to input and jump
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Jumps unless player is already in air
        if keys[pygame.K_SPACE]:
            if not self.in_air:
                self.jump()
                self.in_air = True

    # Adds jump speed to player direction to simulate jump
    def jump(self):
        self.direction.y = self.jump_speed

