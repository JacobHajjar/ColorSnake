#!/usr/bin/env python3
'''My own remake of the classic video game Snake in Pygame'''
from collections import namedtuple
import pygame
from scenes import MenuScene, ScoresScene, SnakeScene
pygame.init()

__author__ = 'Jacob Hajjar'
__email__ = 'hajjarj@csu.fullerton.edu'
__maintainer__ = 'jacobhajjar'

Colors = namedtuple(
    'Colors', ['black', 'lgray', 'white', 'red', 'yellow', 'blue', 'lime', 'aqua', 'purple'])


class SnakeGame:
    '''class for the main logic of the program'''
    colors = Colors((0, 0, 0), (100, 100, 100), (255, 255, 255), (255,   0,   0), (255, 255,   0),
                    (0,  0, 255), (0, 255,   0), (0, 255, 255), (128,  0, 128))
    window_width = 800
    window_height = 640
    title = 'SNAKE'
    display_surf = pygame.display.set_mode((window_width, window_height))
    next_scene = 0
    pygame.display.set_caption(title)

    def play_snake(self):
        '''function which plays a round of snake'''
        snake_fps = 15
        while True:
            if self.next_scene == 0:
                menu = MenuScene(self.colors, self.display_surf, 30)
                snake_fps = menu.start_scene()
                self.next_scene = menu.next_scene
            elif self.next_scene == 1:
                score_scene = ScoresScene(self.colors, self.display_surf, 30)
                score_scene.start_scene()
                self.next_scene = score_scene.next_scene
            elif self.next_scene == 2:
                game_scene = SnakeScene(
                    self.colors, self.display_surf, snake_fps)
                game_scene.start_scene()
                self.next_scene = game_scene.next_scene


def main():
    '''the main function to run the game'''
    game1 = SnakeGame()
    game1.play_snake()


if __name__ == '__main__':
    main()
