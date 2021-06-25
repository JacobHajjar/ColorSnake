'''class file that keeps track of the game's time and points'''
import math
import pygame
import pickle
from datetime import date

class TimerScore:
    '''class that adds score every 2 seconds and can save it to a file'''
    high_scores = []
    def __init__(self, tick_time_ms, score):
        self.tick_time_ms = tick_time_ms
        self.start_time = pygame.time.get_ticks()
        self.begin_count = self.start_time
        self.score = score

    def add_timer_points(self):
        '''function which checks if the amount of time has passed and adds points'''
        current_time = pygame.time.get_ticks()
        points_per_interval = 5
        if current_time >= self.begin_count + self.tick_time_ms:
            self.score += points_per_interval
            print(self.score)
            self.begin_count = current_time

    def add_points(self, points):
        self.score += points

    def save_scores(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        minutes = math.floor((pygame.time.get_ticks() - self.start_time) / 60000)
        print("TIME: ", minutes)
        game_data = [minutes, d1, self.score]
        with open('game_data.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)