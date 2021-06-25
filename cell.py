'''class file for the grid'''
import pygame


class Cell():
    '''class defining a cell in the snake grid'''
    is_food = False
    is_snake = False

    def __init__(self, grid_box, grid_color, cell_col, cell_row):
        self.grid_box = grid_box
        self.grid_color = grid_color
        self.cell_row = cell_row
        self.cell_col = cell_col

    def draw_cell(self, display_surf, color):
        '''draws a snake cell if it is a snake'''
        if self.is_snake:
            pygame.draw.rect(display_surf, color, self.grid_box, 0)
        else:
            pygame.draw.rect(display_surf, self.grid_color, self.grid_box, 0)

    def draw_food(self, display_surf, color):
        '''displays food on grid if there is food'''
        if self.is_food:
            food_size = 8
            pygame.draw.circle(display_surf, color,
                               self.grid_box.center, food_size)
        elif self.is_food is False and self.is_snake is False:
            pygame.draw.rect(display_surf, self.grid_color, self.grid_box, 0)

    def get_location(self):
        '''returns the location of this cell'''
        return self.cell_col, self.cell_row
