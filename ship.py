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
        self.rect.bottom = self.screen_rect.bottom
        self.moving = 0

    def blitme(self):
        #Рисует корабль в текущей позиции
        self.screen.blit(self.image, self.rect)
    
    def update(self, ai_settings: Settings):
        if self.moving == 1:
            if self.rect.centerx < ai_settings.screen_width:
                self.rect.centerx += 2
        
        elif self.moving == -1:
            if self.rect.centerx > 0:
                self.rect.centerx -= 2
        
