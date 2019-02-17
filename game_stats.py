class GameStats():
    """Отслеживание статистики"""
    def __init__(self, ai_settings):
        """Иницилизация статистики"""
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()


    def reset_stats(self):
        """Иницилиазирует статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
