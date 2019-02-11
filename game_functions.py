import pygame

from settings import Settings
from ship import Ship


def check_events(ship) -> bool:
    """Проверяет события связанные с нажатием кнопок клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        check_keydown_events(event, ship)
        check_keyup_events(event, ship)

    return False


def check_keydown_events(event, ship) -> None:
    """Проверяет события связанные с нажатием на кнопку"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving = 1
            
        if event.key == pygame.K_LEFT:
            ship.moving = -1


def check_keyup_events(event, ship) -> None:
    """Проверяет события связанные с высвобождением кнопки"""
    if event.type == pygame.KEYUP:
        ship.moving = 0


def update_screen(ai_settings: Settings, screen, ship: Ship) -> None:
    """Перерисовывает экран"""
    screen.fill(ai_settings.bg_color)
    ship.update(ai_settings)
    ship.blitme()

    #Отображение последнего прорисованого экрана
    pygame.display.flip()