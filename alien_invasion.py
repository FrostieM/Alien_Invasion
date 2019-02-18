import pygame

from settings import Settings
from game_functions import GameFunctions
from button import Button

def run_game():
    """Иницилизация игры и создание объекта окна"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    game_fun = GameFunctions(screen, ai_settings)

    while True:
        if game_fun.check_events(play_button):
            return

        game_fun.update_screen(play_button)


run_game()
