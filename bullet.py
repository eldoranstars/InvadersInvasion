from ammo import Ammo

class Bullet():
    def __init__(self, screen, settings, ship):
        # Атрибуты класса
        self.screen = screen
        self.settings = settings
        self.speed_factor = settings.bullet_sf
        # Загрузка изображения и получение прямоугольника
        self.surface = settings.bullet_surface
        self.surface.fill(settings.bullet_color)
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top - settings.bullet_height
        self.start_position = self.rect.top

    def update(self):
        # Обновление координат изображения
        self.rect.y -= self.speed_factor
        if not self.screen.rect.colliderect(self.rect):
            self.settings.bullets.remove(self)
        for boss in self.settings.bosses:
            if boss.rect.contains(self.rect):
                boss.life_left -= 1
                try:
                    self.settings.bullets.remove(self)
                # если пуля попала сразу в оба объекта
                except: ValueError
        for invader in self.settings.invaders:
            if invader.rect.contains(self.rect):
                self.settings.invaders.remove(invader)
                self.settings.score += 3
                try:
                    self.settings.bullets.remove(self)
                # если пуля попала сразу в оба объекта
                except: ValueError
        for small in self.settings.smalls:
            if small.rect.contains(self.rect):
                self.settings.smalls.remove(small)
                self.settings.score += 3
                try:
                    self.settings.bullets.remove(self)
                # если пуля попала сразу в оба объекта
                except: ValueError
        for eye in self.settings.eyes:
            if eye.rect.contains(self.rect):
                try:
                    self.settings.bullets.remove(self)
                # если пуля попала сразу в оба объекта
                except: ValueError
        for ball in self.settings.balls:
            if ball.rect.contains(self.rect):
                ball.life_left -= 1
                if ball.life_left == 0:
                    ammo = Ammo(self.screen, self.settings, 'shield')
                    ammo.rect.center = ball.rect.center
                    self.settings.ammos.append(ammo)
                    self.settings.balls.remove(ball)
                    self.settings.score += 15
                    self.settings.ball_chance = self.settings.ball_chance * self.settings.ball_chance_reduction
                try:
                    self.settings.bullets.remove(self)
                # если пуля попала сразу в оба объекта
                except: ValueError

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)