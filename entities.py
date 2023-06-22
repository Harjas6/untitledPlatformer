import time

import pygame
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
        self.speed = 8
        self.jump_speed = -10
        self.gravity = 0.8

    # Updates player
    def update(self):
        self.input()
        self.move()

    # Moves player
    def move(self):
        # Changes player position
        self.rect.x += self.direction.x * self.speed
        self.apply_grav()

    def apply_grav(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Sets x direction according to input
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.direction.y = self.jump_speed


