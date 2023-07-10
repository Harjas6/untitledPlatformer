import sys
import pygame
from level import Level
from settings import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF)
        self.level = Level()
        self.clock = pygame.time.Clock()

    def run(self):
        self.level.run()
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
                game_over = pygame.image.load('images/game_over.png')
                game_over = pygame.transform.scale(game_over, (512,256))
                self.screen.fill('blue')
                self.screen.blit(game_over, (WIDTH/3, HEIGHT/3))
                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
