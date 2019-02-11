import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления пулями"""

    def __init__(self, screen, ship, ai_settings):
        """Создает объект пули в текущей позиции корабля"""
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y_pos = float(self.rect.top)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self) -> None:
        """Перемещение пули вверх по экрану"""
        self.y_pos -= self.speed_factor
        self.rect.y = self.y_pos

    
    def draw_bullet(self) -> None:
        """Вывод пули на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        
