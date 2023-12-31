import math
import pygame
from random import randint
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
        self.health = 5
        self.invincible = False
        self.can_dash = False
        self.time = pygame.time.get_ticks()


    # Loads all converted png and places in dictionary
    def load_pngs(self):
        idle = ['idle', 'idle2']
        idle = self.png_loader(idle)
        left = ['left', 'left2', 'left3']
        left = self.png_loader(left)
        right = ['right', 'right2', 'right3']
        right = self.png_loader(right)
        jump = ['jump', 'jump2']
        jump = self.png_loader(jump)
        return {'idle': [idle], 'left': [left], 'right': [right], 'jump': [jump]}

    # Loads pngs according to names given
    def png_loader(self, names):
        animations = []
        for name in names:
            img = pygame.image.load(f"images/player/{name}.png").convert_alpha()
            img = pygame.transform.scale(img, (64, 64))
            animations.append(img)

        return animations

    # Grabs user input
    def update(self):
        self.input()
        self.invincible_status()


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
        if keys[pygame.K_x] and self.can_dash:
            self.dash()

    # Adds jump speed to player direction to simulate jump
    def jump(self):
        self.direction.y = self.jump_speed

    # Causes player character to dash
    def dash(self):
        if pygame.time.get_ticks() - self.time > 700:
            if self.direction.x == 0:
                self.rect.x += DASH_DIST
            else: self.rect.x += self.direction.x * DASH_DIST
            self.time = pygame.time.get_ticks()


    # Makes player invincible for time period
    def invincible_status(self):
        if self.invincible:
            time_passed = pygame.time.get_ticks() - self.time
            if time_passed > 2000:
                self.invincible = False

    # return true if health == 0
    def is_dead(self):
        if self.health == 0:
            return True
        else: return False

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
            self.image = animation[math.floor(self.anim_index)]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_time, speed = 4, horizontal = True, dmg = 1):
        super().__init__()
        self.image = pygame.image.load('images/groundL_enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.patrol_time = patrol_time
        self.time_passed = pygame.time.get_ticks()
        self.direction = 1
        self.speed = speed
        self.horizontal = horizontal

        # dmg included in case I want to refactor enemies into having different amounts of damages
        self.dmg = dmg



    def update(self,shift):
        self.move(shift)

    def move(self, shift):
        self.patrol()
        if self.horizontal:
            self.rect.x += self.direction * self.speed
            self.rect.x += shift[0]
            self.rect.y += shift[1]
        else:
            self.rect.y += self.direction * self.speed
            self.rect.x += shift[0]
            self.rect.y += shift[1]


    def patrol(self):
        if pygame.time.get_ticks() - self.time_passed > self.patrol_time:
            self.time_passed = pygame.time.get_ticks()
            self.direction *= -1


