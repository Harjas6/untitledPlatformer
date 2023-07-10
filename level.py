import pygame
from pytmx import load_pygame

import debugger
from entities import Player, Enemy
from settings import *


class Level():
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.game_over = False
        self.tmx_data = load_pygame('level/tmx/untitledPlatformerTile1.tmx')
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.world_shift = pygame.math.Vector2()
        self.shift_amount = 8
        self.heart = pygame.image.load('images/heart.png')
        self.heart = pygame.transform.scale(self.heart, (48,48))
        self.create_level()

    # Reads tmx file to create level
    def create_level(self):
        layers = self.tmx_data.visible_layers
        for layer in layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    self.tiles.add(Tile(pos=pos, surf=surf))
        self.player.add(Player((300,900)))
        self.enemies.add(Enemy((400,1600),1000))
        self.tiles.draw(self.display)




    # Runs the level
    def run(self):

        # scroll camera
        self.scroll_cam()


        # updates tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display)

        # enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display)

        # Updates player position and collisons
        self.player.update()
        self.collisons()
        self.player.draw(self.display)

        # draws health
        self.draw_health()

    # Draws amnount if health on screen
    def draw_health(self):
        offset = 10
        player = self.player.sprite

        for health in range(player.health):
            self.display.blit(self.heart, (offset, 10))
            offset += 58

    # Scrolls cam in x and y directions
    def scroll_cam(self):
        self.scroll_x()
        self.scroll_y()

    # If player is on horizontal edges of screen moves background accordingly
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direct_x = player.direction.x
        if player_x < WIDTH/3 and direct_x < 0:
            self.world_shift.x = self.shift_amount
            player.rect.x += self.shift_amount
        elif player_x > WIDTH*2/3 and direct_x > 0:
            self.world_shift.x = -self.shift_amount
            player.rect.x += -self.shift_amount

        else:
            self.world_shift.x = 0

    # If player is on vertical edges of screen moves background accordingly
    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direct_y = player.direction.y
        if player_y < HEIGHT*1/5 and direct_y < 0:
            self.world_shift.y = self.shift_amount
            player.rect.y += self.shift_amount
        elif player_y > HEIGHT*5/6:
            self.world_shift.y = -self.shift_amount
            player.rect.y += -self.shift_amount
        else:
            self.world_shift.y = 0

    # All collsions
    def collisons(self):
        self.horiz_tiles_collide()
        self.vert_tiles_collide()
        self.enemies_collision()

    # Checks if players x position collides with any tiles and if not touching any tiles sets player in_air True
    def horiz_tiles_collide(self):
        player = self.player.sprite
        player.move()
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    return None
                elif player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    return None
        player.in_air = True

    # Checks if players y position collides with any tiles and if not touching any tiles sets player in_air True
    def vert_tiles_collide(self):
        player = self.player.sprite
        player.apply_grav()
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.in_air = False
                    return None
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    return None
        player.in_air = True

    def enemies_collision(self):
        player = self.player.sprite

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect) and not player.invincible:
                player.time = pygame.time.get_ticks()
                player.health -= 1
                player.invincible = True
        player_dead = player.is_dead()
        if player_dead:
            self.game_over = True

class Tile(pygame.sprite.Sprite):
    # Creates a block with an image specified by name and places it in a group(s)
    def __init__(self, pos, surf,):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    # Moves tile according to shift
    def update(self, shift):
        self.rect.x += shift.x
        self.rect.y += shift.y