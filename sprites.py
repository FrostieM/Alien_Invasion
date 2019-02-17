import os
import abc

import pygame
from pygame.sprite import Sprite
from settings import Settings


class StandartSpriteOnScreen(abc.ABC):
    """
    Стандартный класс содержащий спрайт, от которого будут наследоваться
    остальные спрайты, которые будут использоваться в данной программе
    """
    def __init__(self, screen, ai_settings, file: str):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #Загрузка изображения
        current_path = os.path.dirname(__file__)
        file_dir = os.path.join(current_path, 'images')
        self.image = pygame.image.load(os.path.join(file_dir, file))
        self.rect = self.image.get_rect()


    def blitme(self):
        """Вывод пришельца в текущей позиции"""
        self.screen.blit(self.image, self.rect)


    @abc.abstractmethod
    def update(self):
        pass


class Alien(StandartSpriteOnScreen, Sprite):
    """Класс задающий функционал врагу"""
    def __init__(self, screen, ai_settings: Settings):
        """Иницилизация основных свойств пришельца"""
        super().__init__(screen, ai_settings, "alien.png")
        #Каждый новый пришелец появляеться в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Сохранение точной позиции пришельца
        self.x_pos = float(self.rect.x)


    def update(self):
        """Перемещает пришельцев вправо"""
        self.x_pos += (self.ai_settings.alien_speed_factor *
                       self.ai_settings.fleet_direction)
        self.rect.x = self.x_pos


    def check_edges(self) -> bool:
        screen_rect = self.screen.get_rect()

        if self.rect.left >= screen_rect.right - 50 or self.rect.left <= 0:
            return True

        return False


class Ship(StandartSpriteOnScreen):
    """Реализация корабля, который будет отображен на экране"""
    def __init__(self, screen, ai_settings: Settings):
        super().__init__(screen, ai_settings, "ship.png")
        #Установка позиции корабля
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.moving = 0


    def update(self) -> None:
        """Обновляет позицию корабля"""
        self.center += self.moving * self.ai_settings.ship_speed_factor

        if self.center < 0:
            self.center = 0

        if self.center > self.ai_settings.screen_width:
            self.center = self.ai_settings.screen_width

        self.rect.centerx = self.center


    def center_ship(self):
        """Размещает корабль в центре"""
        self.center = self.screen_rect.centerx
