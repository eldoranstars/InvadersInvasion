import random

class Asteroid():
    def __init__(self, screen, settings, center):
        # Атрибуты класса
        self.reload_asteroid = False
        self.reload_asteroid_time = 10000
        self.asteroid_left = 0
        self.screen = screen
        self.settings = settings
        self.speed_factor = settings.asteroid_sf
        # Загрузка изображения и получение прямоугольника
        self.surface = random.choice(settings.asteroid_surfaces)
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.center = center

    def update(self):
        # Обновление координат изображения
        for small in self.settings.smalls:
            if self.settings.collision(small.rect, 0.8, 0.6).colliderect(self.settings.collision(self.rect, 0.7, 0.7)):
                self.settings.asteroids.remove(self)
                self.settings.smalls.remove(small)
                self.settings.score += 3

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)