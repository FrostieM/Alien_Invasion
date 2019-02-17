from time import sleep

import pygame

from settings import Settings
from sprites import Ship
from bullet import Bullet
from sprites import Alien


def check_events(ai_settings, screen, ship, bullets, aliens,
                 stats, play_button) -> bool:
    """Проверяет события связанные с нажатием кнопок клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_button = play_button.rect.collidepoint(mouse_x, mouse_y)
            check_play_start(ai_settings, screen, stats,
                              ship, aliens, 
                              bullets, start_button)

        if check_keydown_events(event, ship, screen, 
                                ai_settings, bullets,
                                stats, aliens):
            return True

        check_keyup_events(event, ship)

    return False


def check_play_start(ai_settings, screen, stats,
                     ship, aliens, bullets, condiction):
    """Запускает новую игру при нажатии кнопки Play"""
    if not stats.game_active and condiction:
        stats.game_active = True
        stats.reset_stats()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        pygame.mouse.set_visible(False)
        ai_settings.initialize_dynamic_settings()


def check_keydown_events(event, ship, screen, ai_settings,
                         bullets, stats, aliens) -> None:
    """Проверяет события связанные с нажатием на кнопку"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            fire_bullets(screen, ship, ai_settings, bullets)

        if event.key == pygame.K_RIGHT:
            ship.moving = 1
            
        if event.key == pygame.K_LEFT:
            ship.moving = -1

       
        if event.key == pygame.K_q:
            return True
        
        if event.key == pygame.K_p:
            check_play_start(ai_settings, screen, stats,
                             ship, aliens, bullets, True)
    
    return False


def fire_bullets(screen, ship, ai_settings, bullets) -> None:
    if len(bullets) < ai_settings.bullets_alowed:
        new_bullet = Bullet(screen, ship, ai_settings)
        bullets.add(new_bullet)


def check_keyup_events(event, ship) -> None:
    """Проверяет события связанные с высвобождением кнопки"""
    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
            ship.moving = 0


def update_screen(ai_settings: Settings, screen,
                  ship: Ship, aliens, bullets,
                  stats, play_button, scoreboard) -> None:
    """Перерисовывает экран"""
    screen.fill(ai_settings.bg_color)
    scoreboard.show_score()

    if stats.game_active:
        ship.update()
        ship.blitme()

        update_bullets(ai_settings, stats, screen,
                       ship, aliens, bullets, scoreboard)
        update_aliens(ai_settings, ship, aliens, stats, screen, bullets)
        
        aliens.draw(screen)

    elif not stats.game_active:
        play_button.draw_button()

    #Отображение последнего прорисованого экрана
    pygame.display.flip()


def update_bullets(ai_settings, stats, screen, 
                   ship, aliens, bullets,
                   scoreboard) -> None:
    """Обновляет позицию пуль и удаляет выходящие за границу"""
    bullets.update()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, stats, screen,
                                  ship, aliens, bullets, scoreboard)


def  check_bullet_alien_collisions(ai_settings, stats, screen,
                                   ship, aliens, bullets,
                                   scoreboard):
    if not aliens:
        sleep(0.5)
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.increase_speed()

    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        stats.score += ai_settings.alien_points * len(collisions)
        scoreboard.prep_score()


def update_aliens(ai_settings, ship, aliens, stats, screen, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обработывает столкновение корабля с пришельцем"""
    stats.ship_left -= 1

    aliens.empty()
    bullets.empty()
    
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    if stats.ship_left < 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    sleep(0.5)
    

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def create_fleet(ai_settings, screen, ship, aliens) -> None:
    """Создает флот пришельцев"""
    alien = Alien(screen, ai_settings)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    #Создание первого ряда пришельцев
    for row_number in range(number_rows - 1):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещаемых на экране"""
    available_space_y = (
        ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x_pos = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x_pos
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
