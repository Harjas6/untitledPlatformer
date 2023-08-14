import sys
import pygame

import debugger
from level import *
from settings import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF)
        self.level = Level_1('level/tmx/untitledPlatformerTile1.tmx')
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('blue')
            if not self.level.game_over:
                self.level.run()
                self.clock.tick(FPS)
                pygame.display.update()
            else:
                game_over = pygame.image.load('images/games_over.png')
                self.screen.fill('blue')
                self.screen.blit(game_over, (WIDTH/3, HEIGHT/3))
                self.handle_keys()
                pygame.display.update()

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.level = Level_1('level/tmx/untitledPlatformerTile1.tmx')
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
