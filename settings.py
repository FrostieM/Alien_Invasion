class Settings():
    #Класс для хранения всех настроек игры

    def __init__(self):
        #Настройки экрана
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (67, 27, 140)
        #Настройки корабля
        self.ship_speed_factor = 2.2
        self.ship_limit = 3
        #Настройки пули
        self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (200, 0, 0)
        self.bullets_alowed = 3
        #настройка пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        