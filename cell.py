import pygame
pygame.init()


class Cell():
    '''class defining a cell in the snake grid'''

    def __init__(self, grid_box, is_snake, grid_color, cell_col, cell_row):
        self.grid_box = grid_box
        self.is_snake = is_snake
        self.grid_color = grid_color
        self.cell_row = cell_row
        self.cell_col = cell_col

    def draw_cell(self, display_surf, color):
        if self.is_snake:
            pygame.draw.rect(display_surf, color, self.grid_box, 0)
        else:
            pygame.draw.rect(display_surf, self.grid_color, self.grid_box, 0)
    
    def get_location(self):
        return self.cell_col, self.cell_row
