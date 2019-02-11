import pygame

from settings import Settings
from ship import Ship

def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving = 1
            
            if event.key == pygame.K_LEFT:
                ship.moving = -1
        
        elif event.type == pygame.KEYUP:
            ship.moving = 0

    return False

def update_screen(ai_settings: Settings, screen, ship: Ship):
    screen.fill(ai_settings.bg_color)
    ship.update(ai_settings)
    ship.blitme()

    #Отображение последнего прорисованого экрана
    pygame.display.flip()