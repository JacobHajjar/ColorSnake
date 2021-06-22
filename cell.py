import pygame
pygame.init()

class Cell():
    '''class defining a cell in the snake grid'''
    def __init__(self, grid_box, is_snake):
        self.grid_box = grid_box
        self.is_snake = is_snake
    