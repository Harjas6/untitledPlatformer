import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):
    disp_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'black')
    debug_rect = debug_surf.get_rect(topleft= (x, y))
    pygame.draw.rect(disp_surf, 'white', debug_rect)
    disp_surf.blit(debug_surf, debug_rect)
