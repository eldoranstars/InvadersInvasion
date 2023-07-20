import random

class Tusk():
    def __init__(self, screen, settings, midbottom):
        # Атрибуты класса
        self.screen = screen
        self.settings = settings
        self.speed_factor = settings.tusk_sf
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.tusk_surface
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.midbottom = midbottom

    def update(self):
        # Обновление координат изображения
        self.rect.centery += self.speed_factor
        if not self.screen.rect.colliderect(self.rect):
            self.settings.tusks.remove(self)
            self.settings.score += 3

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)