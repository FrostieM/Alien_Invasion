import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    """Иницилизация игры и создание объекта окна"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_settings)
    ship = Ship(screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    play_button = Button(ai_settings, screen, "Play")
    scoreboard = Scoreboard(ai_settings, screen, stats)

    while True:
        if gf.check_events(ai_settings, screen, ship, bullets, aliens,
                           stats, play_button):
            return
        
        gf.update_screen(ai_settings, screen, ship, aliens, 
                         bullets, stats, play_button, scoreboard)
        

run_game()
