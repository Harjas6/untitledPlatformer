import math
import pygame
from settings import *


# represents the user player
class Player(pygame.sprite.Sprite):
    # creates a player in the given position and set atrributes
    def __init__(self, pos):
        super().__init__()
        self.animations = self.load_pngs()
        self.image = self.animations['idle'][0][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.anim_index = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = SPEED
        self.jump_speed = -16
        self.in_air = True
        self.gravity = 0.8


    # Loads all converted png and places in dictionary
    def load_pngs(self):
        idle = self.load_idle()
        left = self.load_left()
        right = self.load_right()
        jump = self.load_jump()
        return {'idle': [idle], 'left': [left], 'right': [right], 'jump': [jump]}


    # Loads idle pngs
    def load_idle(self):
        names = ['idle', 'idle2']
        return self.png_loader(names)

    # Loads leftward pngs
    def load_left(self):
        names = ['left', 'left2', 'left3']
        return self.png_loader(names)

    # Loads rightward pngs
    def load_right(self):
        names = ['right', 'right2', 'right3']
        return self.png_loader(names)

    # Loads jumping pngs
    def load_jump(self):
        names = ['jump', 'jump2']
        return self.png_loader(names)

    # Loads pngs according to names given
    def png_loader(self, names):
        animations = []
        for name in names:
            img = pygame.image.load(f"images/{name}.png").convert_alpha()
            img = pygame.transform.scale(img, (64, 64))
            animations.append(img)

        return animations

    # Grabs user input
    def update(self):
        self.input()

    # Moves player
    def move(self):
        self.rect.x += self.direction.x * self.speed

    # Applies gravity to player
    def apply_grav(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Sets direction according to input and jumps. Plays appropriate animation alongside
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.cycle_img('left')
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.cycle_img('right')

        else:
            self.direction.x = 0
            self.cycle_img('idle')

        # Jumps unless player is already in air
        if keys[pygame.K_SPACE]:
            if not self.in_air:
                self.jump()
                self.in_air = True

    # Adds jump speed to player direction to simulate jump
    def jump(self):
        self.direction.y = self.jump_speed

    # If player in air runs jump animations otherwise runs animation according to direction
    def cycle_img(self, key, anim_speed=0.15):
        animations = self.animations.get(key)
        if self.in_air:
            self.iterate_animations(self.animations.get('jump'))
        else:
            self.iterate_animations(animations)

    # picks an frame according to floor of index and bumps up the index by anim_speed
    def iterate_animations(self, animations, anim_speed=0.15):
        for animation in animations:
            self.anim_index += anim_speed
            if self.anim_index > len(animation):
                self.anim_index = 0
            self.image = animation[math.floor(math.floor(self.anim_index))]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/blob.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
