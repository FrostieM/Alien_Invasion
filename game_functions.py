import pygame

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

    return False

def update_screen(ai_settings, screen, ship):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    
    #Отображение последнего прорисованого экрана
    pygame.display.flip()