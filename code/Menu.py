#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, COLOR_PINK, MENU_OPTION, COLOR_BLUE


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/menu1.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        pygame.mixer_music.load('./asset./melodia.wav')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Run", COLOR_PINK, ((WIN_WIDTH / 2), 40))
            self.menu_text(50, "Fluffy", COLOR_PINK, ((WIN_WIDTH / 2), 100))

            for i in range(len(MENU_OPTION)):
                self.menu_text(20, MENU_OPTION[i], COLOR_BLUE, ((WIN_WIDTH / 2), 200 + 25 * i))

            pygame.display.flip()

            # Check all for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # close window
                    quit()  # end pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Cambria", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


