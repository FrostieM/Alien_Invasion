import sys

import pygame

def run_game():
    #Иницилизация игры и создание объекта окна
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Alien Invasion")

    while True:
        #Отслеживание событий с клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        #Отображение последнего прорисованого экрана
        pygame.display.flip()

run_game()