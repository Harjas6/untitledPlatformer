import pygame
from pytmx import load_pygame
from entities import Player
from settings import *


class Level():
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.tmx_data = load_pygame('level/tmx/untitledPlatformerTile1.tmx')
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.create_level()
        self.world_shift = pygame.math.Vector2()
        self.shift_amount = 8


    def create_level(self):
        layers = self.tmx_data.visible_layers
        for layer in layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    self.tiles.add(Tile(pos=pos, surf=surf))
                    self.player.add(Player((300,650)))
        self.tiles.draw(self.display)

    def run(self):
        self.scroll()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display)
        self.player.update()
        self.horiz_collisons()
        self.vert_collisons()
        self.player.draw(self.display)


    def scroll(self):
        self.scroll_x()
        self.scroll_y()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direct_x = player.direction.x
        if player_x < WIDTH/3 and direct_x < 0:
            self.world_shift.x = self.shift_amount
            player.rect.x += self.shift_amount
            player.speed = 0
        elif player_x > WIDTH*2/3 and direct_x > 0:
            self.world_shift.x = -self.shift_amount
            player.rect.x += -self.shift_amount
            player.speed = 0

        else:
            self.world_shift.x = 0
            player.speed = 8

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direct_y = player.direction.y
        if player_y < HEIGHT*1/5 and direct_y < 0:
            self.world_shift.y = self.shift_amount
            player.rect.y += self.shift_amount
            player.speed = 0
        elif player_y > HEIGHT*5/6:
            self.world_shift.y = -self.shift_amount
            player.rect.y += -self.shift_amount
            player.speed = 0
        else:
            self.world_shift.y = 0
            player.speed = 8


    def horiz_collisons(self):
        player = self.player.sprite
        player.move()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                elif player.direction.x < 0:
                    player.rect.left = tile.rect.right


    def vert_collisons(self):
        player = self.player.sprite
        player.apply_grav()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.has_jumped = False
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0


class Tile(pygame.sprite.Sprite):
    # Creates a block with an image specified by name and places it in a group(s)
    def __init__(self, pos, surf,):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


    def update(self, shift):
        self.rect.x += shift.x
        self.rect.y += shift.y