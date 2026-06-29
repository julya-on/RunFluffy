#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Background import Background
from code.Const import WIN_WIDTH


class EntityFactory:

      @staticmethod
      def get_entity(entity_name: str, position=(0, 0)):
         match entity_name:
            case 'menu':
             list_menu = []
             # Usando apenas as camadas: 1, 3 e 4
             for i in [1, 3, 4]:
                list_menu.append(Background(f'menu{i}', (0, 0)))
                list_menu.append(Background(f'menu{i}', (WIN_WIDTH, 0)))
             return list_menu

            case 'gato':
              from code.CatPlayer import CatPlayer
              return CatPlayer('cat', (200, 260))

            case 'cachorro':
                from code.DogEnemy import DogEnemy
                return DogEnemy('dog', (50, 260))

            case 'bola':
                from code.YarnBall import YarnBall
                import random
                random_x = random.randint(700, 1000)
                random_y = random.randint(150, 280)
                return YarnBall('ball', (random_x, random_y))

            case _:
                return None