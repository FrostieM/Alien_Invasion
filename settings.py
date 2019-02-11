class Settings():
    #Класс для хранения всех настроек игры

    def __init__(self):
        #Настройки экрана
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (67, 27, 140)
        #Настройки корабля
        self.ship_speed_factor = 2.2
        #Настройки пули
        self.bullet_speed_factor = 1
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (200, 0, 0)
        