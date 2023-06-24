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
        self.jump_speed = -16
        self.gravity = 0.8

    # Updates player
    def update(self):
        self.input()


    # Moves player
    def move(self):
        self.rect.x += self.direction.x * self.speed


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
            self.jump()

    def jump(self):
        self.direction.y = self.jump_speed

    # if object collide with player puts player on correct side of object
    def place_player(self,direc, tile):
        if tile.rect.colliderect(self.rect):
            match direc:
                case 'on top':
                    self.rect.bottom = tile.rect.top
                case 'below':
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 1
                case 'on the right':
                    self.rect.left = tile.rect.right
                case 'on the left':
                    self.rect.right = tile.rect.left
