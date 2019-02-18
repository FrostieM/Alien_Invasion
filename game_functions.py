from time import sleep

import pygame

from settings import Settings
from bullet import Bullet
from sprites import Alien, Ship
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard

class GameFunctions():
    """Realization of basic functionality"""
    def __init__(self, screen, ai_settings: Settings):
        """Creating main variables"""
        self.__screen = screen
        self.__ai_settings = ai_settings
        self.__ship = Ship(screen, ai_settings)
        self.__bullets = pygame.sprite.Group()
        self.__aliens = pygame.sprite.Group()
        self.create_fleet()
        self.__stats = GameStats(ai_settings)
        self.__scoreboard = Scoreboard(ai_settings, screen, self.__stats)


    def check_events(self, play_button: Button) -> bool:
        """Check event of pressing buttons or mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_button = play_button.rect.collidepoint(mouse_x, mouse_y)
                self.check_play_start(condiction=start_button)

            if self.check_keydown_events(event):
                return True

            self.check_keyup_events(event)

        return False


    def check_play_start(self, condiction=True):
        """Check game for active and start it"""
        if not self.__stats.game_active and condiction:
            self.__stats.game_active = True
            self.__stats.reset_stats()
            self.__aliens.empty()
            self.__bullets.empty()
            self.create_fleet()
            self.__ship.center_ship()
            pygame.mouse.set_visible(False)
            self.__ai_settings.initialize_dynamic_settings()


    def check_keydown_events(self, event) -> None:
        """Check event of pressing button"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.fire_bullets()

            if event.key == pygame.K_RIGHT:
                self.__ship.moving = 1

            if event.key == pygame.K_LEFT:
                self.__ship.moving = -1

            if event.key == pygame.K_q:
                return True

            if event.key == pygame.K_p:
                self.check_play_start()

        return False


    def fire_bullets(self) -> None:
        """Generate start of shooting"""
        if len(self.__bullets) < self.__ai_settings.bullets_alowed:
            self.__bullets.add(Bullet(self.__screen, self.__ship,
                                      self.__ai_settings))


    def check_keyup_events(self, event) -> None:
        """Check event of release button"""
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                self.__ship.moving = 0


    def update_screen(self, play_button: Button) -> None:
        """Update and redraws screen"""
        self.__screen.fill(self.__ai_settings.bg_color)
        self.__scoreboard.show_score()

        if self.__stats.game_active:
            self.__ship.update()
            self.__ship.blitme()

            self.update_bullets()
            self.update_aliens()

            self.__aliens.draw(self.__screen)

        else:
            play_button.draw_button()

        pygame.display.flip()


    def update_bullets(self) -> None:
        """Update bullets position and check collisions"""
        self.__bullets.update()

        for bullet in self.__bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.__bullets.copy():
            if bullet.rect.bottom <= 0:
                self.__bullets.remove(bullet)

        self.check_bullets_alien_collisions()


    def  check_bullets_alien_collisions(self):
        """Checking bullets collision with Alien and update score if it was"""
        if not self.__aliens:
            sleep(0.5)
            self.__bullets.empty()
            self.create_fleet()
            self.__ai_settings.increase_speed()

        collisions = pygame.sprite.groupcollide(self.__aliens, self.__bullets,
                                                True, True)
        
        if collisions:
            self.__stats.score += self.__ai_settings.alien_points * len(collisions)
            self.__scoreboard.prep_score()


    def update_aliens(self):
        """Update Alien fleet position and change fleet direction if fleet 
        reached the end of the screen
        """
        self.check_fleet_edges()
        self.__aliens.update()

        if pygame.sprite.spritecollideany(self.__ship, self.__aliens):
            self.ship_hit()

        self.check_aliens_bottom()


    def check_fleet_edges(self):
        """Reacts on screen edges and change fleet direction"""
        for alien in self.__aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break


    def check_aliens_bottom(self):
        """Checking that fleet reached the bottom and if it was 
        then removed ship
        """
        screen_rect = self.__screen.get_rect()
    
        for alien in self.__aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break


    def ship_hit(self):
        """Removed ship live and if lives no more game is over"""
        self.__stats.ship_left -= 1

        self.__aliens.empty()
        self.__bullets.empty()
    
        self.create_fleet()
        self.__ship.center_ship()

        if self.__stats.ship_left < 0:
            self.__stats.game_active = False
            pygame.mouse.set_visible(True)

        sleep(0.5)


    def change_fleet_direction(self):
        for alien in self.__aliens.sprites():
            alien.rect.y += self.__ai_settings.fleet_drop_speed

        self.__ai_settings.fleet_direction *= -1


    def create_fleet(self) -> None:
        """Counting fleet and create every alien ship on position with shift"""
        alien = Alien(self.__screen, self.__ai_settings)
        number_aliens_x = self.get_number_aliens_x(alien.rect.width)
        number_rows = self.get_number_rows(self.__ship.rect.height,
                                           alien.rect.height)
    
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)


    def get_number_aliens_x(self, alien_width):
        """Counting amount of Aliens in row"""
        available_space_x = self.__ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x


    def get_number_rows(self, ship_height, alien_height):
        """Counting amount of Alien columns"""
        available_space_y = (
            self.__ai_settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows


    def create_alien(self, alien_number, row_number):
        alien = Alien(self.__screen, self.__ai_settings)
        alien_width = alien.rect.width
        alien.x_pos = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x_pos
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.__aliens.add(alien)
