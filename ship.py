import os

import pygame

from settings import Settings

class Ship():
    
    def __init__(self, screen):
        self.screen = screen
        
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'images')
        self.image = pygame.image.load(os.path.join(image_path, 'ship.png'))
        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.moving = 0

    def blitme(self):
        #Рисует корабль в текущей позиции
        self.screen.blit(self.image, self.rect)
    
    def update(self, ai_settings: Settings):
        self.center += self.moving * ai_settings.ship_speed_factor
        
        if self.center < 0:
            self.center = 0
        
        if self.center > ai_settings.screen_width:
            self.center = ai_settings.screen_width

        self.rect.centerx = self.center

