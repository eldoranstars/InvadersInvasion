import random
import pygame
from small import Small

class Eye():
    def __init__(self, screen, settings):
        # Атрибуты класса
        self.reload_small = False
        self.last_small_time = 0
        self.reload_small_time = 1000
        self.small_left = 0
        self.screen = screen
        self.settings = settings
        self.speed_factor = random.randrange(int(settings.eye_sf_min), int(settings.eye_sf_max))
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.eye_surface
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = random.randrange(0, screen.rect.right, screen.rect.right)
        self.rect.centery = random.randrange(0, screen.rect.centery / 2, self.rect.height)
        if self.rect.centerx == 0:
            self.move_left = False
        if self.rect.centerx == screen.rect.right:
            self.move_left = True

    def update(self):
        # Обновление координат изображения
        if self.move_left:
            self.rect.centerx -= self.speed_factor
        if not self.move_left:
            self.rect.centerx += self.speed_factor
        if not self.screen.rect.collidepoint(self.rect.midright):
            self.move_left = True
        if not self.screen.rect.collidepoint(self.rect.midleft):
            self.move_left = False
        # Создание флота
        if self.small_left > 0:
            self.small_left -= 1
            self.small = Small(self.screen, self.settings, self.rect.center)
            self.settings.smalls.append(self.small)
        # Флаг перезарядки и фиксация времени начала
        if not self.reload_small and self.small_left == 0:
            self.reload_small = True
            self.last_small_time = pygame.time.get_ticks()
        # Снятие флага перезарядки на основе дельты времени и пополнение боезапаса
        if self.reload_small and pygame.time.get_ticks() - self.last_small_time > self.reload_small_time:
            self.reload_small = False
            self.small_left = 1

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)