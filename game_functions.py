import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, ship, bullets) -> bool:
    """Проверяет события связанные с нажатием кнопок клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        if check_keydown_events(event, ship, screen, ai_settings, bullets):
            return True

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
            fire_bullets(screen, ship, ai_settings, bullets)

        if event.key == pygame.K_q:
            return True
    
    return False


def fire_bullets(screen, ship, ai_settings, bullets):
    if len(bullets) < ai_settings.bullets_alowed:
        new_bullet = Bullet(screen, ship, ai_settings)
        bullets.add(new_bullet)


def check_keyup_events(event, ship) -> None:
    """Проверяет события связанные с высвобождением кнопки"""
    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
            ship.moving = 0


def update_screen(ai_settings: Settings, screen,
                  ship: Ship, aliens, bullets) -> None:
    """Перерисовывает экран"""
    screen.fill(ai_settings.bg_color)
    ship.update(ai_settings)
    update_bullets(bullets)
    ship.blitme()
    aliens.draw(screen)
    #Отображение последнего прорисованого экрана
    pygame.display.flip()


def update_bullets(bullets):
    """Обновляет позицию пуль и удаляет выходящие за границу"""
    bullets.update()

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def create_fleet(ai_settings, screen, aliens):
    """Создает флот пришельцев"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_spcae_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_spcae_x / (2 * alien_width))

    #Создание первого ряда пришельцев
    for alien_number in range(number_aliens_x):
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
