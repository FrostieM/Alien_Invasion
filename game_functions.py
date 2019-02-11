import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


def check_events(ai_settings, screen, ship, bullets) -> bool:
    """Проверяет события связанные с нажатием кнопок клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        check_keydown_events(event, ship, screen, ai_settings, bullets)
        check_keyup_events(event, ship)

    return False


def check_keydown_events(event, ship, screen,
                         ai_settings, bullets) -> None:
    """Проверяет события связанные с нажатием на кнопку"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving = 1
            
        if event.key == pygame.K_LEFT:
            ship.moving = -1

        if event.key == pygame.K_SPACE:
            new_bullet = Bullet(screen, ship, ai_settings)
            bullets.add(new_bullet)

def check_keyup_events(event, ship) -> None:
    """Проверяет события связанные с высвобождением кнопки"""
    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT): 
            ship.moving = 0
            

def update_screen(ai_settings: Settings, screen,
                  ship: Ship, bullets) -> None:
    """Перерисовывает экран"""
    screen.fill(ai_settings.bg_color)
    ship.update(ai_settings)
    bullets.update()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    #Отображение последнего прорисованого экрана
    pygame.display.flip()