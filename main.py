import sys
import pygame

import debugger
from level import *
from settings import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF)
        self.player = Player((0,0))
        self.level = Level_0('levels/tutorial/tmx/untitledPlatformerTutorial.tmx', 250,self.player)
        self.clock = pygame.time.Clock()
        self.level_num = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('blue')


            if self.level.next_level:
                self.level_num +=1
                self.level = self.choose_level(self.player)

            elif not self.level.game_over:
                self.level.run()
                self.clock.tick(FPS)
                pygame.display.update()

            else:
                game_over = pygame.image.load('images/game_over.png')
                self.screen.fill('blue')
                self.screen.blit(game_over, (WIDTH/3, HEIGHT/3))
                self.handle_keys()
                pygame.display.update()

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.player = Player((0,0))
            self.level = Level_0('levels/tutorial/tmx/untitledPlatformerTutorial.tmx',250,self.player)
            self.level_num=0
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    def choose_level(self,player):
        player.direction.x = 0
        player.direction.y = 0
        match self.level_num:
            case 1: return Level_1('levels/level1/tmx/untitledPlatformerLevel1.tmx',500,player)
            case 2: return Level_2('levels/level2/tmx/untitledPlatformerLevel2.tmx',3000,player)



if __name__ == '__main__':
    game = Game()
    game.run()
