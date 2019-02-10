import pygame

from settings import Settings
from ship import Ship

def run_game():
    #Иницилизация игры и создание объекта окна
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen)

    while True:
        #Отслеживание событий с клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(ai_settings.bg_color)
        ship.blitme()
        #Отображение последнего прорисованого экрана
        pygame.display.flip()

run_game()
