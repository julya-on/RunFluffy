#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

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
        self.font = pygame.font.SysFont('Cambria', 22, bold=True)

        self.sound_bark= pygame.mixer.Sound('./asset./dog_bark.wav')
        self.sound_meow = pygame.mixer.Sound('./asset./cat_meow.wav')

        self.sound_bark.set_volume(0.2)
        self.sound_meow.set_volume(0.7)

    def run(self):

        while True:

            self.clock.tick(60)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            gato = None
            cachorro = None
            bola = None

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
                    bola = ent


            # Inteligência do cachorro
            if cachorro is not None and gato is not None:

                if getattr(gato, 'is_moving', False):

                    # Cachorro permanece no canto esquerdo
                    if cachorro.rect.x > 30:
                        cachorro.rect.x -= 2
                    elif cachorro.rect.x < 30:
                        cachorro.rect.x = 30

                else:

                    # Gato parou, cachorro persegue
                    if cachorro.rect.x < gato.rect.x:
                        cachorro.rect.x += 2


            # Trava da tela
            largura = self.window.get_width()

            if gato is not None:
                if gato.rect.right > largura:
                    gato.rect.right = largura

            if cachorro is not None:
                if cachorro.rect.right > largura:
                    cachorro.rect.right = largura


            # Colisão gato e bola
            if gato is not None and bola is not None:

                rect_bola = bola.rect.inflate(-20, -20)

                if gato.rect.colliderect(rect_bola):

                    bola.rect.x = 850
                    bola.rect.y = 270
                    bola.subindo = True

                    self.score += 1


            # Colisão cachorro e gato
            if gato is not None and cachorro is not None:

                if gato.rect.colliderect(cachorro.rect):

                    if not getattr(gato, 'is_moving', False):

                       # Toca os sons
                       self.sound_bark.play()
                       self.sound_meow.play()
                       # Pontuação reinicia
                       self.score = 0

                       cachorro.rect.x = 0


            # Exibe o placar na tela
            score_surf = self.font.render(
                f'Bolas: {self.score}',
                True,
                (250, 250, 250)
            )

            self.window.blit(score_surf, (5, 5))

            pygame.display.flip()
