#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Const import WIN_WIDTH

pygame.mixer.init()

from code.CatPlayer import CatPlayer
from code.DogEnemy import DogEnemy
from code.YarnBall import YarnBall
from code.Entity import Entity
from code.EntityFactory import EntityFactory


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.entity_list: list[Entity] = []

        # Backgrounds
        self.entity_list.extend(EntityFactory.get_entity('menu'))

        # Personagens
        self.entity_list.append(EntityFactory.get_entity('cachorro'))
        self.entity_list.append(EntityFactory.get_entity('gato'))
        self.entity_list.append(EntityFactory.get_entity('bola'))

        self.timeout = 20000
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.SysFont('Cambria', 15, bold=True)

        self.sound_bark= pygame.mixer.Sound('./asset./dog_bark.wav')
        self.sound_meow = pygame.mixer.Sound('./asset./cat_meow.wav')

        self.sound_bark.set_volume(0.9)
        self.sound_meow.set_volume(0.9)

    def run(self):

        while True:
            # Atualiza o tempo restante de jogo
            self.clock.tick(60)
            self.timeout -= self.clock.get_time()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            gato = None
            cachorro = None
            bolas = []

            # Limpa a tela
            self.window.fill((0, 0, 0))

            # Loop principal do jogo
            for ent in self.entity_list:
                ent.move()
                self.window.blit(ent.surf, ent.rect)

                if isinstance(ent, CatPlayer):
                    gato = ent

                elif isinstance(ent, DogEnemy):
                    cachorro = ent

                elif isinstance(ent, YarnBall):
                    bolas.append(ent)

            # Inteligência do cachorro
            if cachorro is not None and gato is not None:

                # Se o gato estiver parado e próximo do lado esquerdo
                if gato.rect.x <= 150 and not getattr(gato, 'is_moving', False):

                     # Cachorro persegue o gato
                    if cachorro.rect.x < gato.rect.x:
                            cachorro.rect.x += 3

                    # Cachorro late apenas se o gato não miar.
                    if not pygame.mixer.get_busy():
                            self.sound_bark.play()

                else:
                    # Se o gato estiver andando, o cachorro retorna para o canto esquerdo
                    if cachorro.rect.x > 30:
                            cachorro.rect.x -= 2
                    else:
                            cachorro.rect.x = 30

            # Trava da tela
            largura = self.window.get_width()

            if gato is not None:
                if gato.rect.right > largura:
                    gato.rect.right = largura

            if cachorro is not None:
                if cachorro.rect.right > largura:
                    cachorro.rect.right = largura


            # Colisão gato e bolas
            if gato is not None:
                for b in bolas:

                   rect_bola = b.rect.inflate(-20, -20)

                   if gato.rect.colliderect(rect_bola):

                      import random

                      b.rect.x = WIN_WIDTH + random.randint(50, 350)
                      b.rect.y = random.randint(150, 270)
                      b.subindo = True

                      self.score += 1

            # Colisão gato e cachorro
            if gato is not None and cachorro is not None:

                if gato.rect.colliderect(cachorro.rect):

                   # Toca os sons
                   self.sound_bark.play()
                   self.sound_meow.play() # O gato mia ao colidir com o cachorro.

                   self.window.fill((0, 0, 0))

                   font_go = pygame.font.SysFont('Cambria', 35, bold=True)

                   go_surf = font_go.render(
                       'GAME OVER',
                       True,
                       (255, 0, 0)
                   )
                   go_rect = go_surf.get_rect(
                       center=(
                           self.window.get_width() // 2,
                           self.window.get_height() // 2
                       )
                   )
                   self.window.blit(go_surf, go_rect)
                   pygame.display.flip()

                   pygame.time.delay(2000)
                   pygame.mixer.stop()

                   return self.score

            # Tempo restante em segundos
            tempo = max(0, self.timeout // 1000)
            if tempo <= 0:
               self.window.fill((0, 0, 0)) # tela preta de game over.
               font_time = pygame.font.SysFont('Cambria', 40, bold=True)

               time_surf = font_time.render(
                   'TEMPO ESGOTADO!',
                   True,
                   (255, 253, 85)
               )
               time_rect = time_surf.get_rect(
                   center=(
                       self.window.get_width() // 2,
                       self.window.get_height() // 2
                   )
               )

               self.window.blit(time_surf, time_rect)

               pygame.display.flip()

               pygame.time.delay(2000)

               pygame.mixer.stop()

               return self.score

            # Exibe o placar na tela
            score_surf = self.font.render(f'Balls: {self.score}', True, (255, 255, 255))

            timer_surf = self.font.render(f'Time: {tempo}s', True, (255, 255, 255))

            # Placar
            self.window.blit(score_surf, (20, 5))

            # Temporizador
            self.window.blit(timer_surf, (20, 25))

            pygame.display.flip()