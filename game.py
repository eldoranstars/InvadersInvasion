import pygame
import game_functions as gf
from stats import GameStats

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Invaders Invasion")
clock = pygame.time.Clock()
stats = GameStats()

while True:
    clock.tick(60)
    if pygame.joystick.get_count():
        joystick = pygame.joystick.Joystick(0)
    gf.check_events(stats, joystick='')
    gf.blit_screen(stats)
    if stats.final_active and not stats.game_active:
        gf.update_final_text()
        gf.append_messages()
    if stats.game_active:
        gf.update_ship(stats, joystick='')
        gf.update_bosses(stats)
        gf.update_invaders(stats)
        gf.update_smalls(stats)
        gf.update_asteroids(stats)
        gf.update_tusks(stats)
        gf.update_balls(stats)
        gf.update_ammos(stats)
        gf.update_eyes(stats)
        gf.update_bullets()
        gf.update_drop_stars()
        gf.append_star()
        if stats.shield_active:
            gf.append_eye()
        if stats.weapon_active:
            gf.append_ball()
        if not stats.boss_active:
            gf.append_invader()
        if not stats.weapon_active:
            gf.append_ammo()