import sys
sys.path.append('rects')
import pygame
import random
from time import sleep
from invader import Invader
from eye import Eye
from ball import Ball
from bullet import Bullet
from settings import Settings
from screen import Screen
from ship import Ship
from fire import Fire
from star import Star
from text import Text
from ammo import Ammo
from boss import Boss

settings = Settings()
screen = Screen(settings)
ship = Ship(screen, settings)
fire = Fire(screen, settings)
star = Star(screen, settings)
pause = Text(screen, "PAUSE: Q", screen.rect.centerx, screen.rect.centery - 44)
record = Text(screen, "PREVIOS RECORD: {:,}", screen.rect.centerx, screen.rect.centery - 22)
score = Text(screen, "SCORE: {:,}", screen.rect.centerx, screen.rect.centery)
buttons = [pause, record, score]
collision = settings.collision

def overlap(player, enemy):
    # Получаем пиксельную маску для обработки коллизий.
    player.mask = pygame.mask.from_surface(player.surface)
    enemy.mask = pygame.mask.from_surface(enemy.surface)
    overlap = player.mask.overlap(enemy.mask, (enemy.rect.left - player.rect.left, enemy.rect.top - player.rect.top))
    return overlap

def collision_test(object, wm, hm):
    # Вывод коллизий на экран.
    screen.surface.blit(pygame.Surface((collision(object.rect, wm, hm).width,collision(object.rect, wm, hm).height)), collision(object.rect, wm, hm))

def check_events(stats, joystick):
    # Отслеживание событий клавиатуры и мыши.
    if stats.game_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                stats.game_active = False
                score.update_text(settings.score)
            if joystick:
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(7) == 1:
                    stats.game_active = False
                    score.update_text(settings.score)
    if not stats.game_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if stats.music_active:
                    stats.music_active = False
                    pygame.mixer.pause()
                else:
                    stats.music_active = True
                    pygame.mixer.unpause()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                stats.game_active = True
                if stats.final_active:
                    stats.final_active = False
                    ship.surface = settings.ship_surface
                    settings.new_game()
            if joystick:
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6) == 1:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(5) == 1:
                    if stats.music_active:
                        stats.music_active = False
                        pygame.mixer.pause()
                    else:
                        stats.music_active = True
                        pygame.mixer.unpause()
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4) == 1:
                    pygame.display.toggle_fullscreen()
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(7) == 1:
                    stats.game_active = True
                    if stats.final_active:
                        stats.final_active = False
                        ship.surface = settings.ship_surface
                        settings.new_game()

def update_ship(stats, joystick):
    # Отслеживание нажатий клавиатуры и мыши.
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT] == 1 and ship.rect.right < settings.screen_width:
        ship.rect.centerx += settings.ship_sf
        fire.rect.centerx += settings.fire_sf
    if key[pygame.K_LEFT] == 1 and ship.rect.left > 0:
        ship.rect.centerx -= settings.ship_sf
        fire.rect.centerx -= settings.fire_sf
    if key[pygame.K_UP] == 1 and ship.rect.top > 0:
        ship.rect.centery -= settings.ship_sf
        fire.rect.centery -= settings.fire_sf
    if key[pygame.K_DOWN] == 1 and ship.rect.bottom < settings.screen_height:
        ship.rect.centery += settings.ship_sf
        fire.rect.centery += settings.fire_sf
    if key[pygame.K_SPACE] == 1 and settings.bullet_left > 0:
        settings.bullet_left -= 1
        bullet = Bullet(screen, settings, ship)
        settings.bullets.append(bullet)
        settings.bullet_sound.play()
    if joystick:
        if joystick.get_axis(0) and joystick.get_axis(0) > 0.2 and ship.rect.right < settings.screen_width:
            ship.rect.centerx += settings.ship_sf
            fire.rect.centerx += settings.fire_sf
        if joystick.get_axis(0) and joystick.get_axis(0) < -0.2 and ship.rect.left > 0:
            ship.rect.centerx -= settings.ship_sf
            fire.rect.centerx -= settings.fire_sf
        if joystick.get_axis(1) and joystick.get_axis(1) < -0.2 and ship.rect.top > 0:
            ship.rect.centery -= settings.ship_sf
            fire.rect.centery -= settings.fire_sf
        if joystick.get_axis(1) and joystick.get_axis(1) > 0.2 and ship.rect.bottom < settings.screen_height:
            ship.rect.centery += settings.ship_sf
            fire.rect.centery += settings.fire_sf
        if joystick.get_axis(5) > 0.2 and settings.bullet_left > 0:
            settings.bullet_left -= 1
            bullet = Bullet(screen, settings, ship)
            settings.bullets.append(bullet)
            settings.bullet_sound.play()
    if stats.weapon_active:
        # Флаг перезарядки и фиксация времени начала
        if not settings.reload_bullet and settings.bullet_left == 0:
            settings.reload_bullet = True
            settings.last_bullet_time = pygame.time.get_ticks()
        # Снятие флага перезарядки на основе дельты времени и пополнение боезапаса
        if settings.reload_bullet and pygame.time.get_ticks() - settings.last_bullet_time > settings.reload_bullet_time:
            settings.reload_bullet = False
            settings.bullet_left = settings.bullet_limit
    if stats.power_active:
        # Снятие флага перезарядки на основе дельты времени
        if pygame.time.get_ticks() - settings.last_power_time > settings.reload_power_time:
            stats.power_active = False
            settings.reload_bullet_time = settings.reload_bullet_time_limit

def update_fire(stats):
    # Обновить расположение объектов на экране.
    if not stats.final_active:
        fire.update()

def update_invaders(stats):
    # Обновить расположение объектов на экране.
    for invader in settings.invaders:
        invader.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(invader.rect, 0.8, 0.6)):
            settings.invaders.remove(invader)
            reset_after_collision(stats)

def update_smalls(stats):
    # Обновить расположение объектов на экране.
    for small in settings.smalls:
        small.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(small.rect, 0.8, 0.6)):
            settings.smalls.remove(small)
            reset_after_collision(stats)

def update_eyes(stats):
    # Обновить расположение объектов на экране.
    for eye in settings.eyes:
        eye.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(eye.rect, 0.7, 0.7)):
            settings.eyes.remove(eye)
            reset_after_collision(stats)

def update_asteroids(stats):
    # Обновить расположение объектов на экране.
    for asteroid in settings.asteroids:
        asteroid.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(asteroid.rect, 0.7, 0.7)):
            settings.asteroids.remove(asteroid)
            reset_after_collision(stats)

def update_tusks(stats):
    # Обновить расположение объектов на экране.
    for tusk in settings.tusks:
        tusk.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(tusk.rect, 0.9, 0.6)):
            settings.tusks.remove(tusk)
            reset_after_collision(stats)

def update_bosses(stats):
    # Обновить расположение объектов на экране.
    for boss in settings.bosses:
        boss.update()
        if boss.life_left < 0:
            sleep(0.6)
            stats.final_active = True
            settings.intro_sound.stop()
            settings.outro_sound.play(-1)
            stats.game_active = False
            stats.boss_active = False
            stats.shield_active = False
            stats.weapon_active = False
            if settings.score > settings.record:
                settings.record = settings.score
                record.update_text(settings.record)
            score.update_text(settings.score)
        if overlap(ship, boss):
            reset_after_collision(stats)

def update_balls(stats):
    # Обновить расположение объектов на экране.
    for ball in settings.balls:
        ball.update()
        if not stats.shield_active:
            if collision(ship.rect, 0.6, 0.9).colliderect(collision(ball.rect, 0.7, 0.7)):
                settings.balls.remove(ball)
                reset_after_collision(stats)
        if stats.shield_active:
            if collision(ball.rect, 0.7, 0.7).collidepoint(ship.rect.midtop):
                ball.move_down = False
                ball.surface = settings.alien_ball_surface
            if collision(ball.rect, 0.7, 0.7).collidepoint(ship.rect.midbottom):
                ball.move_down = True
                if ball.speed_factor < settings.ball_sf_max:
                    ball.speed_factor += 1
                ball.surface = settings.alien_ball_surface
            if collision(ball.rect, 0.7, 0.7).collidepoint(ship.rect.midleft):
                ball.move_left = True
                ball.move_right = False
                ball.move_down = False
                ball.surface = settings.alien_ball_surface
            if collision(ball.rect, 0.7, 0.7).collidepoint(ship.rect.midright):
                ball.move_left = False
                ball.move_right = True
                ball.move_down = False
                ball.surface = settings.alien_ball_surface

def update_ammos(stats):
    # Обновить расположение объектов на экране.
    for ammo in settings.ammos:
        ammo.update()
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(ammo.rect, 0.7, 0.7)):
            settings.ammos.remove(ammo)
            if ammo.type == 'weapon':
                stats.weapon_active = True
                settings.invader_sf_min = 1
                settings.invader_sf_max = 8
                settings.bullet_limit = 1
                settings.bullet_left = settings.bullet_limit
                ship.surface = settings.weapon_ship_surface
            if ammo.type == 'shield':
                stats.shield_active = True
                ship.surface = settings.shield_ship_surface
            if ammo.type == 'alien':
                stats.power_active = True
                settings.reload_bullet_time = 150
                settings.score += 1500
                settings.last_power_time = pygame.time.get_ticks()
            if ammo.type == 'brain':
                stats.boss_active = True
                boss = Boss(screen, settings)
                settings.ammos.clear()
                settings.bosses.append(boss)
                settings.ball_chance = 16
                settings.eye_chance = 16

def update_bullets():
    # Обновить расположение объектов на экране.
    for bullet in settings.bullets:
        bullet.update()

def update_drop_stars():
    # Обновить расположение объектов на экране.
    for star in settings.drop_stars:
        star.update()

def update_final_text():
    # Обновить расположение объектов на экране.
    for message in settings.final_text:
        message.scroll_text()

def reset_after_collision(stats):
    # Обновить счет и экран после коллизии
    sleep(0.6)
    if stats.shield_active:
        stats.shield_active = False
        ship.surface = settings.weapon_ship_surface
    else:
        stats.weapon_active = False
        ship.surface = settings.ship_surface
        settings.star_left -= 1
        if len(settings.stars) > 0:
            settings.player_hit()
            drop_star = random.choice(settings.stars)
            settings.stars.remove(drop_star)
            settings.drop_stars.append(drop_star)
            ship.rect.centerx = screen.rect.centerx
            ship.rect.bottom = screen.rect.bottom
            fire.rect.centerx = screen.rect.centerx
            fire.rect.centery = screen.rect.bottom
        else:
            stats.game_active = False
            stats.boss_active = False
            if settings.score > settings.record:
                settings.record = settings.score
                record.update_text(settings.record)
            score.update_text(settings.score)
            settings.new_game()

def append_invader():
    # Создание объектов в списке
    if random.randrange(0,100) < settings.invader_chance and len(settings.invaders) < settings.invader_allowed:
        invader = Invader(screen, settings)
        settings.invaders.append(invader)
        if ship.surface == settings.ship_surface and settings.invader_sf_min < settings.invader_sf_max - 1:
            settings.invader_sf_min += 0.1

def append_ball():
    # Создание объектов в списке
    if random.randrange(0,5000) < settings.ball_chance:
        ball = Ball(screen, settings)
        settings.balls.append(ball)
        settings.ball_chance = settings.ball_chance / settings.ball_chance_reduction

def append_eye():
    # Создание объектов в списке
    if random.randrange(0,5000) < settings.eye_chance:
        eye = Eye(screen, settings)
        settings.eyes.append(eye)
        settings.eye_chance = settings.eye_chance / settings.eye_chance_reduction

def append_ammo():
    # Создание объектов в списке
    if random.randrange(0,1000) < settings.ammo_chance and len(settings.ammos) < settings.ammo_allowed:
        ammo = Ammo(screen, settings, 'weapon')
        settings.ammos.append(ammo)

def append_star():
    # Создание объектов в списке
    if len(settings.stars) < settings.star_left:
        star = Star(screen, settings)
        settings.stars.append(star)
    for star in settings.drop_stars:
        if collision(ship.rect, 0.6, 0.9).colliderect(collision(star.rect, 0.6, 0.6)):
            settings.drop_stars.remove(star)
            settings.stars.append(star)

def append_messages():
    # Создание объектов в списке
    for message in settings.messages:
        settings.first_line += 33
        new_message = Text(screen, message, screen.rect.centerx, screen.rect.bottom + settings.first_line)
        settings.final_text.append(new_message)
    settings.messages.clear()

def blit_screen(stats):
    # Вывод изображений на экран.
    screen.blitme()
    for star in settings.stars:
        star.blitme()
    for star in settings.drop_stars:
        star.blitme()
    for ammo in settings.ammos:
        ammo.blitme()
    ship.blitme()
    fire.blitme()
    for bullet in settings.bullets:
        bullet.blitme()
    for boss in settings.bosses:
        boss.blitme()
    for invader in settings.invaders:
        invader.blitme()
    for asteroid in settings.asteroids:
        asteroid.blitme()
    for tusk in settings.tusks:
        tusk.blitme()
    for small in settings.smalls:
        small.blitme()
    for eye in settings.eyes:
        eye.blitme()
    for ball in settings.balls:
        ball.blitme()
    if not stats.game_active and not stats.final_active:
        for button in buttons:
            button.blitme()
    if stats.final_active:
        for message in settings.final_text:
            message.blitme()
    pygame.display.update()