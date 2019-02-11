import pygame

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    """Иницилизация игры и создание объекта окна"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen)

    while True:
        if gf.check_events(ship):
            return

        gf.update_screen(ai_settings, screen, ship)


run_game()
