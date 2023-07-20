import random

class Small():
    def __init__(self, screen, settings, center):
        # Атрибуты класса
        self.screen = screen
        self.settings = settings
        self.speed_factor = random.randrange(int(settings.small_sf_min), int(settings.small_sf_max))     
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.small_surface
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.center = center

    def update(self):
        # Обновление координат изображения
        self.rect.centery += self.speed_factor
        if not self.screen.rect.colliderect(self.rect):
            self.settings.smalls.remove(self)
            self.settings.score += 1

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)