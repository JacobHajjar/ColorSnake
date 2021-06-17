#!/usr/bin/env python3
'''My own remake of the classic video game Snake'''
import random
import pygame
import sys
from pygame.locals import *
from collections import namedtuple

__author__ = 'Jacob Hajjar'
__email__ = 'hajjarj@csu.fullerton.edu'
__maintainer__ = 'jacobhajjar'

Colors = namedtuple('Colors', ['black', 'white'])
Settings = namedtuple('Settings', ['FPS', 'window_width', 'window_height',
                                   'box_size', 'menu_color', 'bg_color', 'margin_size'])
colors = Colors((0,   0,   0), (255, 255, 255))
settings = Settings(12, 640, 480, 20, colors.white, colors.white, 20)
pygame.init()
fps_clock = pygame.time.Clock()
display_surf = pygame.display.set_mode(
    (settings.window_width, settings.window_height))
title_font = pygame.font.Font('title_font.otf', 80)
title_render = title_font.render('SNAKE', False, colors.black, None)

def main():
    # main function for the snake game

    while True:  # main menu selections loop
        in_game = False
        display_menu()
        while True:  # game started loop
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mousex, mousey = pygame.mouse.get_pos()
            if not in_game:
                display_surf.blit(title_render, [200, 200])
            pygame.display.update()
            fps_clock.tick(settings.FPS)
        break


def display_menu():
    '''function which runs the game's main menu'''
    display_surf.fill(settings.menu_color)
    text_box = title_render.get_rect()
    text_box.center = (200, 150)

def play_game():
    '''function which runs the main snake game'''


if __name__ == '__main__':
    main()
