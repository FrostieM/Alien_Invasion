import pygame

from settings import Settings
from ship import Ship

def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        key_down(event, ship)
        key_up(event, ship)

    return False


def key_down(event, ship):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving = 1
            
        if event.key == pygame.K_LEFT:
            ship.moving = -1


def key_up(event, ship):
    if event.type == pygame.KEYUP:
        ship.moving = 0


def update_screen(ai_settings: Settings, screen, ship: Ship):
    screen.fill(ai_settings.bg_color)
    ship.update(ai_settings)
    ship.blitme()

    #Отображение последнего прорисованого экрана
    pygame.display.flip()