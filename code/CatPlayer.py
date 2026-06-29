#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.Entity import Entity


class CatPlayer(Entity):
    def __init__(self, name:str, position: tuple):
      super().__init__(name, position)


      self.ground_y = position[1]
      self.speed_y = 0  # Pulo do gato
      self.gravity = 0.6
      self.jump_force = -12  # Força do pulo
      self.is_jumping = False
      self.walk_speed = 5  # Movimento horizontal
      self.is_moving = False

    def move(self):
        # Teclas pressionadas
        key = pygame.key.get_pressed()
        self.is_moving = False

        # Movimentando o gato para a direita
        if key[pygame.K_RIGHT]:
           self.rect.x += self.walk_speed # O gato anda para a frente.
           self.is_moving = True
        # Movimentando o gato para a esquerda
        if key[pygame.K_LEFT]:
            self.rect.x -= self.walk_speed
            self.is_moving = True
        # Trava da tela para o gato não ultrapassar
        if self.rect.x > 650:
               self.rect.x = 650

        # Quando pressionar tecla ESPAÇO o gato pula.
        if key[pygame.K_SPACE] and not self.is_jumping:
            self.speed_y = self.jump_force
            self.is_jumping = True

        # Aplica a gravidade e move o gato.
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Após o pulo, colisão com o chão.
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.speed_y = 0
            self.is_jumping = False

