import pygame
from pytmx import load_pygame

import debugger
from entities import Player, Enemy
from settings import *

class Level():
    def __init__(self, level_file):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.get_surface()
        self.game_over = False
        self.tmx_data = load_pygame(level_file)
        self.start_delay = 3000

        self.make_groups()

        self.world_shift = pygame.math.Vector2()
        self.shift_amount = 8

        self.heart = pygame.image.load('images/heart.png')
        self.heart = pygame.transform.scale(self.heart, (48,48))

        self.start_time = pygame.time.get_ticks()
        self.create_level()

    # Makes groups needed for level. Will be specific to each level
    def make_groups(self):
        pass
    def create_level(self):
        pass

    # Draws amount if health on screen
    def draw_health(self):
        offset = 10
        player = self.player.sprite

        for health in range(player.health):
            self.display.blit(self.heart, (offset, 10))
            offset += 58

    # Runs the level
    def run(self):
        self.scroll_cam()
        self.update_screen()

        # doesn't let player move until on screen
        if pygame.time.get_ticks() - self.start_time > self.start_delay:
            self.player.update()

        self.teleport_player()
        self.collisons()
        self.player.draw(self.display)

        # draws health overtop all objects (KEEP LAST)
        self.draw_health()
        debugger.debug(self.player.sprite.rect)

    # Scrolls cam in x and y directions
    def scroll_cam(self):
        return self.scroll_x(), self.scroll_y()

        # If player is on horizontal edges of screen moves background accordingly

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direct_x = player.direction.x
        if player_x < WIDTH / 3 and direct_x < 0:
            self.world_shift.x = self.shift_amount
            player.rect.x += self.shift_amount

        elif player_x > WIDTH * 2 / 3 and direct_x > 0:
            self.world_shift.x = -self.shift_amount
            player.rect.x += -self.shift_amount

        else:
            self.world_shift.x = 0

        # If player is on vertical edges of screen moves background accordingly

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direct_y = player.direction.y
        if player_y < HEIGHT * 1 / 5 and direct_y < 0:
            self.world_shift.y = self.shift_amount
            player.rect.y += self.shift_amount
        elif player_y > HEIGHT * 3 / 5:
            self.world_shift.y = -self.shift_amount
            player.rect.y += -self.shift_amount
        else:
            self.world_shift.y = 0

    def collisons(self):
        pass

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

    # moves camera toward player and turns off player movement for given amount of time(ms)
    # need to be refactored to limit similarities in code!!!
    def recenter(self, length):
        player = self.player.sprite
        player.is_dead()
        if player.is_dead():
            self.game_over = True
            return None
        start = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start < length:

            player.direction.x = 0
            player.direction.y = 0
            player_x = player.rect.centerx
            if player_x < WIDTH / 3:
                self.world_shift.x = self.shift_amount
                player.rect.x += self.shift_amount

            elif player_x > WIDTH * 2 / 3:
                self.world_shift.x = -self.shift_amount
                player.rect.x += -self.shift_amount

            else:
                self.world_shift.x = 0

            player_y = player.rect.centery
            if player_y < HEIGHT * 1 / 5:
                self.world_shift.y = self.shift_amount
                player.rect.y += self.shift_amount
            elif player_y > HEIGHT * 3 / 5:
                self.world_shift.y = -self.shift_amount
                player.rect.y += -self.shift_amount
            else:
                self.world_shift.y = 0
            self.display.fill('blue')
            self.update_screen()
            self.collisons()
            self.player.draw(self.display)
            self.draw_health()
            self.clock.tick(FPS)
            pygame.display.update()


    def calculate_center_time(self, tile):
        tilex = tile.rect.x
        tiley = tile.rect.y
        spawn_point = self.get_point()
        x = spawn_point.rect.x
        y = spawn_point.rect.y
        x_dist = abs(tilex - x)
        y_dist = abs(tiley - y)

        if max(x_dist,y_dist) < 20*32:
            return 500
        elif max(x_dist,y_dist) < 40*32:
            return 1000
        elif max(x_dist,y_dist) < 60*32:
            return 1800
        elif max(x_dist,y_dist) < 80*32:
            return 3500
        elif max(x_dist,y_dist) < 100*32:
            return 7000
        else: return 8000

    def boundary_collisons(self):
        self.sideBoundary()
        self.bottomBoundary()

    def sideBoundary(self):
        player = self.player.sprite

        for tile in self.boundaryVert.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    return None
                elif player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    return None

    def bottomBoundary(self):
        player = self.player.sprite
        spawn_point = self.get_point()
        x = spawn_point.rect.x
        y = spawn_point.rect.y
        for tile in self.boundaryHoriz.sprites():
            if tile.rect.colliderect(player.rect):
                player.time = pygame.time.get_ticks()
                player.health -= 1
                player.invincible = True
                player.rect.x = x
                player.rect.y = y
                length = self.calculate_center_time(tile)
                self.recenter(length)
            player_dead = player.is_dead()
            if player_dead:
                self.game_over = True

    def get_point(self):
        return self.spawnPoint.sprite

class Level_1(Level):

    # Makes groups and attributes
    def make_groups(self):
        self.tiles = pygame.sprite.Group()
        self.boundaryHoriz = pygame.sprite.Group()
        self.boundaryVert = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.spawnPoint = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.teleport_tiles = pygame.sprite.Group()

    # Reads tmx file to create level
    def create_level(self):
        layers = self.tmx_data.visible_layers
        level = 0
        for layer in layers:
            level += 1
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    match level:
                        # level tiles
                        case 1:
                            pos = (x * 32, y * 32)
                            self.tiles.add(Tile(pos=pos, surf=surf))
                        # ground enemies
                        case 2:
                            pos = (x * 32, y * 32)
                            self.enemies.add(Enemy(pos, 2500, speed=2))
                        # projectile enemies
                        case 3:
                            pos = (x * 32, y * 32)
                            self.enemies.add(Enemy(pos, 1500, speed = 3, horizontal=False))
                        # teleport locations
                        case 4:
                            pos = (x * 32, y * 32)
                            self.teleport_tiles.add(Tile(pos=pos, surf=surf))
                        # boundary tiles
                        case 5:
                            pos = (x * 32, y * 32)
                            self.boundaryHoriz.add(Tile(pos=pos, surf=surf))
                        case 6:
                            pos = (x * 32, y * 32)
                            self.boundaryVert.add(Tile(pos=pos, surf=surf))
                        # SpawnPoint
                        case 7:
                            pos = (x * 32, y * 32)
                            self.spawnPoint.add(Tile(pos=pos, surf=surf))

        x = self.spawnPoint.sprite.rect.x
        y = self.spawnPoint.sprite.rect.y
        self.player.add(Player((x,y)))
        self.tiles.draw(self.display)


    # updates all neccessary groups
    def update_screen(self):
        # updates world tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display)

        # keeps spawn Point in line wiht the rest of the tiles
        self.spawnPoint.update(self.world_shift)

        # updates and draws teleport spot
        self.teleport_tiles.update(self.world_shift)
        self.teleport_tiles.draw(self.display)

        # update enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display)

        # Updates both boundary's but keeps it invisible
        self.boundaryHoriz.update(self.world_shift)
        self.boundaryVert.update(self.world_shift)

    # All collsions
    def collisons(self):
        self.horiz_tiles_collide()
        self.vert_tiles_collide()
        self.enemies_collision()
        self.boundary_collisons()


    def enemies_collision(self):
        player = self.player.sprite

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect) and not player.invincible:
                player.time = pygame.time.get_ticks()
                player.health -= enemy.dmg
                player.invincible = True
            player_dead = player.is_dead()
            if player_dead:
                self.game_over = True



    # if player collides with the teleport tile, transports player to new location
    # Returns True if after teleportation, screen needs to be shifted
    def teleport_player(self):
        player = self.player.sprite
        # Not confirmed but seems like Ordered with index 0 being farthest
        # from bottom left(when viewed on Tiled)
        teleport_locations = self.teleport_tiles.sprites()

        if player.rect.colliderect(teleport_locations[3].rect):
            new_location = teleport_locations[0].rect.x, teleport_locations[0].rect.y
            player.direction.x = 0
            player.direction.y = 0
            player.rect.x = new_location[0]
            player.rect.y = new_location[1]
            self.recenter(2000)
            return True

        elif player.rect.colliderect(teleport_locations[2].rect):
            new_location = teleport_locations[1].rect.x, teleport_locations[1].rect.y
            player.direction.x = 0
            player.direction.y = 0
            player.rect.x = new_location[0]
            player.rect.y = new_location[1]
            self.recenter(500)
            return True
        else:
            return False



class Tile(pygame.sprite.Sprite):
    # Creates a block with an image specified by name and places it in a group(s)
    def __init__(self, pos, surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    # Moves tile according to shift
    def update(self, shift):
        self.rect.x += shift[0]
        self.rect.y += shift[1]