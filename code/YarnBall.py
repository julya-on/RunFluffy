#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED, WIN_WIDTH
from code.Entity import Entity


class YarnBall(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Define a velocidade da bola
        self.speed = ENTITY_SPEED['bola']

    def move(self):
        # Move a bola para a esquerda
        self.rect.x -= self.speed

        if not hasattr(self, 'subindo'):
            self.subindo = True

        if self.subindo:
            self.rect.y -= 2
            if self.rect.y <= 130:
                self.subindo = False
        else:
            self.rect.y += 2  # Ajustado para + para descer
            if self.rect.y >= 270:
                self.subindo = True

        if self.rect.right < 0:
            self.rect.x = WIN_WIDTH + 100
            self.rect.y = 270
            self.subindo = True
