#!/usr/bin/env python3
'''My own remake of the classic video game Snake in Pygame'''
from collections import namedtuple
import pygame
from scenes import MenuScene, SnakeScene
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
    window_width = 640
    window_height = 480
    display_surf = pygame.display.set_mode((window_width, window_height))
    title = 'SNAKE'
    next_scene = 0
    pygame.display.set_caption(title)

    def play_snake(self):
        '''function which plays a round of snake'''
        menu = MenuScene(self.colors, self.display_surf)
        game_scene = SnakeScene(self.colors, self.display_surf)
        scenes = [menu, game_scene]
        while True:
            if self.next_scene is 1:
                scenes[1].generate_snake_grid()
            scenes[self.next_scene].start_scene()
            self.next_scene = scenes[self.next_scene].next_scene
            print("SCENE CHANGED!!")


def main():
    '''the main function to run the game'''
    game1 = SnakeGame()
    game1.play_snake()


if __name__ == '__main__':
    main()
