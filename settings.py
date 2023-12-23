import pygame
import sys
import os

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Settings():
    def __init__(self):
        pygame.init()
        # Параметры игры
        self.star_limit = 3
        self.record = 0
        self.boss_score = 4444
        self.ship_sf = 4
        self.fire_sf = self.ship_sf
        self.star_sf = self.ship_sf - 1
        # Параметры экрана
        self.screen_width = 480
        self.screen_height = 720
        self.screen_color = (100, 100, 100)
        # Параметры пули
        self.bullet_width = 3
        self.bullet_height = 9
        self.bullet_sf = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_limit = 1
        self.reload_bullet_time_limit = 900
        # Параметры изображений
        self.screen_bg = pygame.image.load(resource_path('media/space.png'))
        self.star_surface = pygame.image.load(resource_path('media/star.png'))
        self.ship_surface = pygame.image.load(resource_path('media/ship.png'))
        self.fire1_surface = pygame.image.load(resource_path('media/fire1.png'))
        self.fire2_surface = pygame.image.load(resource_path('media/fire2.png'))
        self.fire3_surface = pygame.image.load(resource_path('media/fire3.png'))
        self.fire4_surface = pygame.image.load(resource_path('media/fire4.png'))
        self.fire5_surface = pygame.image.load(resource_path('media/fire5.png'))
        self.fire6_surface = pygame.image.load(resource_path('media/fire6.png'))
        self.fire_surfaces = [self.fire1_surface, self.fire2_surface, self.fire3_surface, \
                                self.fire4_surface, self.fire5_surface, self.fire6_surface]
        self.weapon_ship_surface = pygame.image.load(resource_path('media/weapon-ship.png'))
        self.shield_ship_surface = pygame.image.load(resource_path('media/shield-ship.png'))
        self.alien_ball_surface = pygame.image.load(resource_path('media/alien-ball.png'))
        self.invader_surface = pygame.image.load(resource_path('media/invader.png'))
        self.small_surface = pygame.image.load(resource_path('media/small.png'))
        self.tusk_surface = pygame.image.load(resource_path('media/tusk.png'))
        self.ball_surface = pygame.image.load(resource_path('media/ball.png'))
        self.boss100_surface = pygame.image.load(resource_path('media/boss100.png'))
        self.boss75_surface = pygame.image.load(resource_path('media/boss75.png'))
        self.boss50_surface = pygame.image.load(resource_path('media/boss50.png'))
        self.boss25_surface = pygame.image.load(resource_path('media/boss25.png'))
        self.boss00_surface = pygame.image.load(resource_path('media/boss00.png'))
        self.eye_surface = pygame.image.load(resource_path('media/eye.png'))
        self.ammo_surface = pygame.image.load(resource_path('media/laser-gun.png'))
        self.alien_surface = pygame.image.load(resource_path('media/alien.png'))
        self.brain_surface = pygame.image.load(resource_path('media/brain.png'))
        self.shield_surface = pygame.image.load(resource_path('media/space-gun.png'))
        self.asteroid_pink = pygame.image.load(resource_path('media/asteroid-pink.png'))
        self.asteroid_grey = pygame.image.load(resource_path('media/asteroid-grey.png'))
        self.asteroid_blue = pygame.image.load(resource_path('media/asteroid-blue.png'))
        self.screen_surface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED)
        self.bullet_surface = pygame.Surface((self.bullet_width, self.bullet_height))
        # Параметры аудио
        self.bullet_sound = pygame.mixer.Sound(resource_path('media/bullet.mp3'))
        self.intro_sound = pygame.mixer.Sound(resource_path('media/intro.mp3'))
        self.outro_sound = pygame.mixer.Sound(resource_path('media/outro.mp3'))
        # Параметры чужих
        self.boss_sf = self.ship_sf - 2
        self.tusk_sf = 5
        self.small_sf_min = 1
        self.small_sf_max = 8
        self.invader_chance = 10
        self.invader_allowed = 15
        self.ball_sf_min = 2
        self.ball_sf_max = 5
        self.ball_chance_reduction = 2
        self.eye_sf_min = 2
        self.eye_sf_max = 5
        self.eye_chance_reduction = 2
        self.asteroid_sf = 4
        self.asteroid_surfaces = [self.asteroid_pink, self.asteroid_grey, self.asteroid_blue]
        # Параметры аммуниции
        self.ammo_sf_min = 1
        self.ammo_sf_max = 2
        self.ammo_chance = 1
        self.ammo_allowed = 1
        # Динамические параметры игры
        self.new_game()

    def player_hit(self):
        # Сбросить параметры при столкновении
        self.smalls.clear()
        self.tusks.clear()
        self.invaders.clear()
        self.eyes.clear()
        self.balls.clear()
        self.bullets.clear()
        self.asteroids.clear()
        self.ammos.clear()
        self.invader_sf_min = 1
        self.invader_sf_max = 9
        self.eye_chance = 8
        self.ball_chance = 16
        self.bullet_left = self.bullet_limit - self.bullet_limit

    def new_game(self):
        # Сбросить параметры для новой игры
        self.final_text = []
        self.smalls = []
        self.tusks = []
        self.invaders = []
        self.eyes = []
        self.balls = []
        self.bullets = []
        self.asteroids = []
        self.ammos = []
        self.stars = []
        self.drop_stars = []
        self.bosses = []
        self.star_left = self.star_limit
        self.score = 0
        self.first_line = 0
        self.reload_power_time = 3300
        self.reload_bullet = False
        self.reload_bullet_time = self.reload_bullet_time_limit
        self.player_hit()
        self.outro_sound.stop()
        self.intro_sound.stop()
        self.intro_sound.play(-1)
        # Титры
        self.messages = ['Producer:', 'eldoranstars', '', \
            'Project Manager:', 'eldoranstars', '', \
            'Game Developer:', 'eldoranstars', '', \
            'Game Designer:', 'eldoranstars', '', \
            'Sound Designer:', 'eldoranstars', '', \
            'Quality Assurance:', 'eldoranstars', '', \
            'Lead DevOps:', 'eldoranstars']

    def collision(self, rect, wm, hm):
        # Получаем дополнительный прямоугольник для обработки коллизий.
        collision = pygame.Rect(rect.center, (rect.width * wm, rect.height * hm))
        collision.center = rect.center
        return collision