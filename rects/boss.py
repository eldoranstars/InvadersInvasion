import random
import pygame
from asteroid import Asteroid
from tusk import Tusk

class Boss():
    def __init__(self, screen, settings):
        # Атрибуты класса
        self.reload_asteroid = False
        self.last_asteroid_time = 0
        self.reload_asteroid_time = 1800
        self.asteroid_left = 0
        self.reload_tusk = False
        self.last_tusk_time = 0
        self.reload_tusk_time = 500
        self.tusk_left = 0
        self.screen = screen
        self.settings = settings
        self.speed_factor = 1
        self.life_limit = 40
        self.life_left = self.life_limit
        self.move_left = False
        self.move_down = True
        self.move_direction = random.randrange(0,2)
        if self.move_direction == 0:
            self.move_left = True
        if self.move_direction == 1:
            self.move_left = False        
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.boss100_surface
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = random.randrange(self.rect.width, settings.screen_width, self.rect.width)
        self.rect.centery = 0

    def update(self):
        # Обновление координат изображения
        if self.speed_factor <= self.settings.boss_sf:
            self.speed_factor += 0.001
        if self.life_left < 0:
            self.surface = self.settings.boss00_surface
        elif self.life_left < self.life_limit * 0.25:
            self.surface = self.settings.boss25_surface
        elif self.life_left < self.life_limit * 0.5:
            self.surface = self.settings.boss50_surface
        elif self.life_left < self.life_limit * 0.75:
            self.surface = self.settings.boss75_surface
        if self.move_left:
            self.rect.centerx -= self.speed_factor
        if not self.move_left:
            self.rect.centerx += self.speed_factor
        if self.move_down:
            self.rect.centery += self.speed_factor
        if not self.move_down:
            self.rect.centery -= self.speed_factor
        if not self.screen.rect.collidepoint(self.rect.midleft):
            self.move_left = False
        if not self.screen.rect.collidepoint(self.rect.midright):
            self.move_left = True
        if not self.screen.rect.collidepoint(self.rect.midbottom):
            self.move_down = False
        if not self.screen.rect.collidepoint(self.rect.midtop):
            self.move_down = True
        # Создание флота
        if self.asteroid_left > 0 and not self.move_down:
            self.asteroid_left -= 1
            if self.settings.eyes:
                self.asteroid = Asteroid(self.screen, self.settings, self.rect.midleft)
                self.settings.asteroids.append(self.asteroid)
                self.asteroid = Asteroid(self.screen, self.settings, self.rect.midright)
                self.settings.asteroids.append(self.asteroid)
            else:
                self.asteroid = Asteroid(self.screen, self.settings, self.rect.center)
                self.settings.asteroids.append(self.asteroid) 
        # Флаг перезарядки и фиксация времени начала
        if not self.reload_asteroid and self.asteroid_left == 0:
            self.reload_asteroid = True
            self.last_asteroid_time = pygame.time.get_ticks()
        # Снятие флага перезарядки на основе дельты времени и пополнение боезапаса
        if self.reload_asteroid and pygame.time.get_ticks() - self.last_asteroid_time > self.reload_asteroid_time:
            self.reload_asteroid = False
            self.asteroid_left = 1
        # Создание флота
        if self.tusk_left > 0 and self.rect.centery < self.settings.screen_height / 4:
            self.tusk_left -= 1
            self.tusk = Tusk(self.screen, self.settings, self.rect.midbottom)
            self.settings.tusks.append(self.tusk)
        # Флаг перезарядки и фиксация времени начала
        if not self.reload_tusk and self.tusk_left == 0:
            self.reload_tusk = True
            self.last_tusk_time = pygame.time.get_ticks()
        # Снятие флага перезарядки на основе дельты времени и пополнение боезапаса
        if self.reload_tusk and pygame.time.get_ticks() - self.last_tusk_time > self.reload_tusk_time:
            self.reload_tusk = False
            self.tusk_left = 1

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)