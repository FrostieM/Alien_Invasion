import os

import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):
    """Класс задающий функционал врагу"""

    def __init__(self, ai_settings: Settings, screen):
        """Иницилизация основных свойств пришельца"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #Загрузка изображения
        current_path = os.path.dirname(__file__)
        file_dir = os.path.join(current_path, 'images')
        self.image = pygame.image.load(os.path.join(file_dir, 'alien.png'))
        self.rect = self.image.get_rect()
        #Каждый новый пришелец появляеться в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Сохранение точной позиции пришельца
        self.x_pos = float(self.rect.x)


    def blitme(self):
        """Вывод пришельца в текущей позиции"""
        self.screen.blit(self.image, self.rect)



