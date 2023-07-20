import pygame
pygame.font.init()

class Text():
    def __init__(self, screen, msg, posx, posy, score = 0):
        # Атрибуты класса
        self.screen = screen
        self.msg = msg
        self.button_color = (150, 150, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 33)
        # Загрузка изображения и получение прямоугольника
        self.update_text(score)
        self.rect = self.surface.get_rect()
        # Получение изначальных координат изображения
        self.rect.centerx = posx
        self.rect.bottom = posy

    def update_text(self, score):
        # Обновление изображения
        self.score_msg = self.msg.format(score)
        self.surface = self.font.render(self.score_msg, True, self.text_color)

    def scroll_text(self):
        # Обновление координат изображения
        self.rect.centery -= 1

    def blitme(self):
        # Вывод изображения на экран
        self.screen.surface.blit(self.surface, self.rect)