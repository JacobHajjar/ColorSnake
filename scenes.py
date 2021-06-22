'''Class containing all of the game's scenes'''

import random
import sys
import pygame
from pygame.locals import *
from cell import Cell
pygame.init()


class MenuScene:
    '''class for the menu scenes of the game'''
    in_scene = True
    curr_mouse = [-1, -1]
    curr_direction = 'up'
    next_scene = 0

    def __init__(self, colors, display_surf):
        self.colors = colors
        self.display_surf = display_surf

    def start_scene(self):
        '''runs the scene in the game'''
        fps = 30
        self.in_scene = True
        self.display_surf.fill(self.colors.white)
        fps_clock = pygame.time.Clock()
        while self.in_scene:  # game started loop
            self.curr_mouse = [-1, -1]
            self.curr_direction = None
            for event in pygame.event.get():  # event handling loop
                #pylint: disable=E0602
                # ^ pylint doesn't like pygame event variables :(
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    self.curr_mouse = [mousex, mousey]
                elif event.type == KEYDOWN:
                    if event.key in (K_LEFT, K_a):
                        self.curr_direction = 'left'
                    elif event.key in (K_RIGHT, K_d):
                        self.curr_direction = 'right'
                    elif event.key in (K_UP, K_w):
                        self.curr_direction = 'up'
                    elif event.key in (K_DOWN, K_s):
                        self.curr_direction = 'down'
            self.display_scene()
            pygame.display.update()
            fps_clock.tick(fps)

    def display_scene(self):
        '''the logic and objects displayed in the scene'''
        width, height = self.display_surf.get_size()
        row_height = height * 5 / 6
        menu_button_size = (160, 40)

        # gray box for decoration
        text_rend, text_box = load_text(
            'title_font.otf', 120, self.colors.black, 'SNAKE')
        self.display_centered_text(text_rend, text_box, (width/2, height/3))

        self.display_centered_rect(
            (width, 70), self.colors.lgray, 0, (width/2, row_height))
        # start button
        start_clicked = self.display_button_click(
            menu_button_size, (width / 2, row_height), self.colors.red, self.colors.black)
        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, 'PLAY')
        self.display_centered_text(
            text_rend, text_box, (width / 2, row_height))
        # game difficulty button
        difficulty_clicked = self.display_button_click(
            menu_button_size, (width / 5, row_height), self.colors.lime, self.colors.black)
        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, 'DIFFICULTY')
        self.display_centered_text(
            text_rend, text_box, (width / 5, row_height))
        # highscore button
        highscore_clicked = self.display_button_click(
            menu_button_size, (width * 4 / 5, row_height), self.colors.aqua, self.colors.black)
        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, 'HIGHSCORE')
        self.display_centered_text(
            text_rend, text_box, (width * 4 / 5, row_height))

        if start_clicked:
            self.next_scene = 1
            self.in_scene = False
        elif difficulty_clicked:
            print("Difficulty Selected")
        elif highscore_clicked:
            print("button3")

    def display_centered_text(self, text_rend, text_box, xycenter_position):
        '''easy function for displaying external text centered'''
        text_box.center = xycenter_position
        self.display_surf.blit(text_rend, text_box)

    def display_left_text(self, text_rend, text_box, xyleft_position):
        '''easy function for displaying text centered left'''
        text_box.center = xyleft_position
        self.display_surf.blit(text_rend, text_box)

    def display_centered_rect(self, xy_size, col, outline_size, xycenter_position):
        '''function for drawing a rectangle centered with coordinates'''
        b_width = xy_size[0]
        b_height = xy_size[1]
        rect_obj = pygame.Rect(0, 0, b_width, b_height)
        rect_obj.center = xycenter_position
        pygame.draw.rect(self.display_surf, col, rect_obj, outline_size)
        return rect_obj

    def display_button_click(self, xy_size, xycenter_position, b_color, o_color):
        '''function for displaying a button that can return a true or false if clicked'''
        o_size = 3
        mousex, mousey = pygame.mouse.get_pos()
        start_button = self.display_centered_rect(
            xy_size, b_color, 0, xycenter_position)
        if start_button.collidepoint(mousex, mousey):
            self.display_centered_rect(
                xy_size, o_color, o_size, xycenter_position)
        if start_button.collidepoint(self.curr_mouse[0], self.curr_mouse[1]):
            return True
        return False


class SnakeScene(MenuScene):
    '''scene for the main snake game'''
    snake_grid = []
    margin = 40
    box_size = 20

    def display_scene(self):
        self.display_surf.fill(self.colors.black)
        width, height = self.display_surf.get_size()

        play_area = self.display_centered_rect(
            (width-self.margin * 2, height-self.margin * 2), 
            self.colors.white, 2, (width/2, height/2))
        self.draw_snake_grid()

    def generate_snake_grid(self):
        '''generates the game grid for snake'''
        width, height = self.display_surf.get_size()
        margin = self.margin
        box_size = self.box_size

        for row in range(margin, width-margin, box_size):
            row_list = []
            for col in range(margin, height-margin, box_size):
                grid_box = pygame.Rect(row, col, box_size, box_size)
                cell = Cell(grid_box, False)
                row_list.append(cell)
                pygame.draw.rect(self.display_surf,
                                 self.colors.red, cell.grid_box, 3)
            self.snake_grid.append(row_list)
    
    def draw_snake_grid(self):
        '''draws the snake grid'''
        for row in self.snake_grid:
            for cell in row:
                print()


def load_text(font, size, col, msg):
    '''function to help load text'''
    font_obj = pygame.font.Font(font, size)
    font_render = font_obj.render(msg, True, col, None)
    #render(text, antialias, color, background=None)
    return font_render, font_render.get_rect()
