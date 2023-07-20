import random
from ammo import Ammo

class Ball():
    def __init__(self, screen, settings):
        # Атрибуты класса
        self.screen = screen
        self.settings = settings
        self.life_left = 4
        self.speed_factor = random.randrange(int(settings.ball_sf_min), int(settings.ball_sf_max))
        self.move_left = False
        self.move_right = False
        self.move_down = True
        self.move_direction = random.randrange(0,9)
        if self.move_direction < 3:
            self.move_left = True
        if self.move_direction > 5:
            self.move_right = True        
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.ball_surface
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = random.randrange(self.rect.width, settings.screen_width, self.rect.width)
        self.rect.centery = 0

    def update(self):
        # Обновление координат изображения
        if self.move_left:
            self.rect.centerx -= self.speed_factor
        if self.move_right:
            self.rect.centerx += self.speed_factor
        if self.move_down:
            self.rect.centery += self.speed_factor
        if not self.move_down:
            self.rect.centery -= self.speed_factor
        if not self.screen.rect.collidepoint(self.rect.midleft):
            self.move_left = False
            self.move_right = True
        if not self.screen.rect.collidepoint(self.rect.midright):
            self.move_right = False
            self.move_left = True
        if not self.screen.rect.collidepoint(self.rect.midbottom):
            self.move_down = False
        if not self.screen.rect.collidepoint(self.rect.midtop) and self.surface == self.settings.ball_surface:
            self.move_down = True
        if not self.screen.rect.colliderect(self.rect):
            self.settings.balls.remove(self)
            self.settings.score += 15
            self.settings.ball_chance = self.settings.ball_chance * self.settings.ball_chance_reduction
        if self.surface == self.settings.alien_ball_surface:
            for boss in self.settings.bosses:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(boss.rect, 0.8, 0.6)):
                    self.settings.balls.remove(self)
                    boss.life_left -= 12
            for invader in self.settings.invaders:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(invader.rect, 0.8, 0.6)):
                    self.settings.invaders.remove(invader)
                    self.settings.score += 3
            for small in self.settings.smalls:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(small.rect, 0.8, 0.6)):
                    self.settings.smalls.remove(small)
                    self.settings.score += 3
            for tusk in self.settings.tusks:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(tusk.rect, 0.9, 0.6)):
                    self.settings.tusks.remove(tusk)
                    self.settings.score += 3
            for asteroid in self.settings.asteroids:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(asteroid.rect, 0.7, 0.7)):
                    self.settings.asteroids.remove(asteroid)
                    self.settings.score += 3
            for eye in self.settings.eyes:
                if self.settings.collision(self.rect, 0.7, 0.7).colliderect(self.settings.collision(eye.rect, 0.7, 0.7)):
                    if self.settings.score > self.settings.boss_score and not self.settings.bosses:
                        ammo = Ammo(self.screen, self.settings, 'brain')
                    else:
                        ammo = Ammo(self.screen, self.settings, 'alien')
                    ammo.rect.center = eye.rect.center
                    self.settings.ammos.append(ammo)
                    self.settings.eyes.remove(eye)
                    self.settings.score += 150
                    self.settings.eye_chance = self.settings.eye_chance * self.settings.eye_chance_reduction
        if self.surface == self.settings.ball_surface:
            for asteroid in self.settings.asteroids:
                if self.settings.collision(self.rect, 0.7, 0.7).collidepoint(asteroid.rect.midtop):
                    self.move_down = False
                if self.settings.collision(self.rect, 0.7, 0.7).collidepoint(asteroid.rect.midbottom):
                    self.move_down = True
                if self.settings.collision(self.rect, 0.7, 0.7).collidepoint(asteroid.rect.midleft):
                    self.move_left = True
                    self.move_right = False
                    self.move_down = False
                if self.settings.collision(self.rect, 0.7, 0.7).collidepoint(asteroid.rect.midright):
                    self.move_left = False
                    self.move_right = True
                    self.move_down = False

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)