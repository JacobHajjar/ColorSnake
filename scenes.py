'''Class containing all of the game's scenes'''
import time
import math
import random
import sys
import pygame
from pygame.locals import *
from cell import Cell
from score import TimerScore
pygame.init()


class MenuScene:
    '''class for the menu scenes of the game'''
    in_scene = True
    curr_mouse = [-1, -1]
    curr_direction = 'up'
    next_scene = 3
    dif_selection = 1
    player_score = None

    def __init__(self, colors, display_surf, fps):
        self.colors = colors
        self.display_surf = display_surf
        self.fps = fps

    def start_scene(self):
        '''runs the scene in the game'''
        self.setup_scene()
        fps_clock = pygame.time.Clock()
        while self.in_scene:  # game started loop
            self.curr_mouse = [-1, -1]
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
                        if self.curr_direction != 'right':
                            self.curr_direction = 'left'
                    elif event.key in (K_RIGHT, K_d):
                        if self.curr_direction != 'left':
                            self.curr_direction = 'right'
                    elif event.key in (K_UP, K_w):
                        if self.curr_direction != 'down':
                            self.curr_direction = 'up'
                    elif event.key in (K_DOWN, K_s):
                        if self.curr_direction != 'up':
                            self.curr_direction = 'down'
            self.display_scene()
            pygame.display.update()
            fps_clock.tick(self.fps)
        return self.dif_selection * 5

    def setup_scene(self):
        '''function which must runs once before the main game loop'''
        self.in_scene = True
        self.dif_selection = 1
        self.player_score = TimerScore(3000, 0)
        try:
            self.player_score.import_scores()
        except FileNotFoundError:
            self.player_score.populate_scores()

    def display_scene(self):
        '''the logic and objects displayed in the scene'''
        self.display_surf.fill(self.colors.white)
        width, height = self.display_surf.get_size()
        row_height = height * 5 / 6
        menu_button_size = (220, 40)

        text_rend, text_box = load_text(
            'title_font.otf', 120, self.colors.black, 'SNAKE')
        self.display_centered_text(text_rend, text_box, (width/2, height/3))
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

        dif_rend, dif_box = load_text(
            'game_over.ttf', 70, self.colors.black, 'DIFFICULTY: ')

        self.display_centered_text(
            dif_rend, dif_box, (width / 5-10, row_height))

        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, str(self.dif_selection))
        self.display_left_text(
            text_rend, text_box, dif_box.bottomright)
        # highscore button
        highscore_clicked = self.display_button_click(
            menu_button_size, (width * 4 / 5, row_height), self.colors.aqua, self.colors.black)
        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, 'HIGHSCORE')
        self.display_centered_text(
            text_rend, text_box, (width * 4 / 5, row_height))

        if start_clicked:
            self.next_scene = 3
            self.in_scene = False
        elif difficulty_clicked:
            if self.dif_selection < 4:
                self.dif_selection += 1
            else:
                self.dif_selection = 1
        elif highscore_clicked:
            self.next_scene = 1
            self.in_scene = False

    def display_centered_text(self, text_rend, text_box, xycenter_position):
        '''easy function for displaying external text centered'''
        text_box.center = xycenter_position
        self.display_surf.blit(text_rend, text_box)

    def display_left_text(self, text_rend, text_box, xyleft_position):
        '''easy function for displaying text centered left'''
        text_box.bottomleft = xyleft_position
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
        o_size = 4
        bor_color = self.colors.lgray
        mousex, mousey = pygame.mouse.get_pos()
        start_button = self.display_centered_rect(
            xy_size, b_color, 0, xycenter_position)
        if start_button.collidepoint(mousex, mousey):
            bor_color = o_color
        self.display_centered_rect(
            xy_size, bor_color, o_size, xycenter_position)

        if start_button.collidepoint(self.curr_mouse[0], self.curr_mouse[1]):
            return True
        return False


class SnakeScene(MenuScene):
    '''scene for the main snake game'''
    snake_grid = []
    snake_body = []
    margin = 40
    food_color = None
    game_color = None
    next_scene = 1
    food_spawned = False
    player_score = None

    def display_scene(self):
        self.player_score.add_timer_points()
        self.display_surf.fill(self.colors.black)
        width, height = self.display_surf.get_size()

        self.spawn_food()
        self.move_snake()
        self.display_centered_rect(
            (width-self.margin * 2, height-self.margin * 2),
            self.game_color, 10, (width/2, height/2))
        score_render, score_box = load_text(
            'game_over.ttf', 75, self.game_color, 'Score: ')
        total_score_rend, total_score_box = load_text(
            'game_over.ttf', 75, self.game_color, str(self.player_score.score))
        score_multi, score_multi_box = load_text(
            'game_over.ttf', 75, self.game_color, "Score multiplier: x")
        multi, multi_box = load_text(
            'game_over.ttf', 75, self.game_color, str(len(self.snake_body)))
        high_score, high_score_box = load_text(
            'game_over.ttf', 75, self.game_color, "HIGH SCORE: ")
        score_num = 0
        if len(self.player_score.scores_data) >= 1:
            score_num = self.player_score.scores_data[0][0]

        high_score_num, high_score_num_text = load_text(
            'game_over.ttf', 75, self.game_color, str(score_num))

        self.display_left_text(score_render, score_box,
                               (self.margin, self.margin-5))
        self.display_left_text(
            total_score_rend, total_score_box, (score_box.right, score_box.bottom))

        self.display_left_text(
            score_multi, score_multi_box, (width/3, height-3))
        self.display_left_text(
            multi, multi_box, (score_multi_box.right, score_multi_box.bottom))

        self.display_left_text(
            high_score, high_score_box, (width/2, self.margin-5))
        self.display_left_text(
            high_score_num, high_score_num_text, (high_score_box.right, high_score_box.bottom))

        self.draw_snake_grid()

    def setup_scene(self):
        '''function which must runs once before the main game loop'''
        self.game_color = self.colors.red
        self.player_score = TimerScore(3000, 0)
        self.player_score.import_scores()
        self.in_scene = True
        self.generate_snake_grid()
        self.create_snake()

    def generate_snake_grid(self):
        '''generates the game grid for snake'''
        self.snake_grid = []
        self.food_spawned = False
        width, height = self.display_surf.get_size()
        margin = self.margin
        box_size = 20
        for col_index, col in enumerate(range(margin, width-margin, box_size)):
            col_list = []
            for row_index, row in enumerate(range(margin, height-margin, box_size)):
                grid_box = pygame.Rect(col, row, box_size, box_size)
                cell = Cell(grid_box, self.colors.black,
                            col_index, row_index)
                col_list.append(cell)
            self.snake_grid.append(col_list)

    def draw_snake_grid(self):
        '''draws the snake grid'''
        if self.in_scene is True:
            for body in self.snake_body:
                col, row = body.get_location()
                self.snake_grid[col][row].is_snake = True
            for col in self.snake_grid:
                for cell in col:
                    cell.draw_cell(self.display_surf, self.game_color)
                    cell.draw_food(self.display_surf, self.food_color)
        else:
            width, height = self.display_surf.get_size()
            self.display_centered_rect((width, height), self.colors.black, 0, (width/2, height/2))
            game_over_text, game_over_box = load_text('game_over.ttf', 80, self.colors.white, 'GAME OVER')
            self.display_centered_text(game_over_text, game_over_box, (width/2, height/2))
            self.fps = 0.4

    def create_snake(self):
        '''function that creates the '''
        self.snake_body = []
        x_grid = math.floor(len(self.snake_grid)/2)
        y_grid = math.floor(len(self.snake_grid[1])/2)
        for i in range(3):
            self.snake_grid[x_grid][y_grid+i].is_snake = True
            self.snake_body.append(self.snake_grid[x_grid][y_grid+i])

    def move_snake(self):
        '''function that moves the snake for one frame'''
        col, row = self.snake_body[0].get_location()
        try:
            if self.curr_direction == 'up':
                self.snake_body.insert(0, self.snake_grid[col][row-1])
                if row == 0 or self.snake_grid[col][row-1].is_snake is True:
                    self.in_scene = False
            elif self.curr_direction == 'down':
                self.snake_body.insert(0, self.snake_grid[col][row+1])
                if self.snake_grid[col][row + 1].is_snake is True:
                    self.in_scene = False
            elif self.curr_direction == 'left':
                self.snake_body.insert(0, self.snake_grid[col-1][row])
                if col == 0 or self.snake_grid[col-1][row].is_snake is True:
                    self.in_scene = False
            elif self.curr_direction == 'right':
                self.snake_body.insert(0, self.snake_grid[col+1][row])
                if self.snake_grid[col + 1][row].is_snake is True:
                    self.in_scene = False
            col, row = self.snake_body[0].get_location()
            if self.snake_grid[col][row].is_food is True:
                self.snake_grid[col][row].is_food = False
                self.food_spawned = False
                self.game_color = self.food_color
                self.player_score.score += 2 * len(self.snake_body)

        except IndexError:
            self.in_scene = False

        col, row = self.snake_body[-1].get_location()
        if self.food_spawned:
            self.snake_grid[col][row].is_snake = False
            self.snake_body.pop()
        if self.in_scene is False:
            self.player_score.save_scores("You")

    def spawn_food(self):
        '''spawns the food when no fodo is present'''
        if self.food_spawned is False:
            while True:
                col = random.randint(0, len(self.snake_grid) - 1)
                row = random.randint(0, len(self.snake_grid[1]) - 1)
                rand_color_index = random.randint(3, len(self.colors) - 1)
                if self.food_color != self.colors[rand_color_index] and self.snake_grid[col][row].is_snake is False:
                    break
            self.food_color = self.colors[rand_color_index]
            self.snake_grid[col][row].is_food = True
            self.food_spawned = True


class ScoresScene(MenuScene):
    '''class for displaying the game's saved high scores'''
    high_scores = None

    def display_scene(self):
        width, height = self.display_surf.get_size()
        row_height = height * 5 / 6
        menu_button_size = (220, 40)
        # play again button
        play_clicked = self.display_button_click(
            menu_button_size, (width / 2, row_height), self.colors.red, self.colors.black)
        text_rend, text_box = load_text(
            'game_over.ttf', 70, self.colors.black, "Play Snake?")
        self.display_centered_text(
            text_rend, text_box, (width / 2, row_height))
        # scoreboard
        title_list = ['High Score', 'Name', 'Seconds', 'Date Played']
        text_size = 55
        title_height = 1/14

        rank_rend, rank_box = load_text(
            'game_over.ttf', text_size, self.colors.black,
            'Ranking#')
        self.display_centered_text(
            rank_rend, rank_box, (width * 1 / 7, height * title_height))
        height_spacer = 1/7
        for i in range(5):
            text_rend, text_box = load_text(
                'game_over.ttf', text_size, self.colors.black, str(i+1))
            self.display_centered_text(
                text_rend, text_box, (width * 1 / 7, height * height_spacer))
            height_spacer += 1/7

        width_spacer = 2/7
        for i, sec_title in enumerate(title_list):
            height_spacer = 1/7
            rend, box = load_text(
                'game_over.ttf', text_size, self.colors.black,
                sec_title)
            self.display_centered_text(
                rend, box, (width * width_spacer, height * title_height))
            for j in range(5):
                text_rend, text_box = load_text(
                    'game_over.ttf', text_size, self.colors.black,
                    str(self.high_scores.scores_data[j][i]))
                self.display_centered_text(
                    text_rend, text_box, (width * width_spacer, height * height_spacer))
                height_spacer += 1/7
            width_spacer += 1/7

        if play_clicked:
            self.in_scene = False
            self.next_scene = 0

    def setup_scene(self):
        self.display_surf.fill(self.colors.white)
        self.next_scene = 0
        self.high_scores = TimerScore(3000, 0)
        self.high_scores.import_scores()
    
class InstructionScene(MenuScene):
    def display_scene(self):
        instruction = pygame.image.load('instructions.jpg')
        self.display_surf.blit(instruction, (0,0))
        self.in_scene = self.player_score.wait_time()
    def setup_scene(self):
        self.player_score = TimerScore(3000, 0)
        self.next_scene = 2


def load_text(font, size, col, msg):
    '''function to help load text'''
    font_obj = pygame.font.Font(font, size)
    font_render = font_obj.render(msg, True, col, None)
    #render(text, antialias, color, background=None)
    return font_render, font_render.get_rect()
