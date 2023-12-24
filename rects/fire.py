import random

class Fire():
    def __init__(self, screen, settings):
        # Атрибуты класса
        self.screen = screen.surface
        self.settings = settings
        self.animation_reload = 0
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.fire_surfaces[0]
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = screen.rect.centerx
        self.rect.centery = screen.rect.bottom

    def update(self):
        # Обновление координат изображения
        self.animation_reload += 1
        if self.animation_reload > 6:
            self.surface = random.choice(self.settings.fire_surfaces)
            self.animation_reload = 0

    def blitme(self):
        # Вывод изображения на экран
        self.screen.blit(self.surface, self.rect)