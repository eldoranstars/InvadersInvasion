class Screen():
    def __init__(self, settings):
        # Атрибуты класса
        self.settings = settings
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.screen_surface
        self.rect = self.surface.get_rect()

    def blitme(self):
        # Вывод изображения на экран
        # self.surface.fill(self.settings.screen_color)
        self.surface.blit(self.settings.screen_bg, self.rect)