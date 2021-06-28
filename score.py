'''class file that keeps track of the game's time and points'''
import math
import pickle
from datetime import date
import pygame


class TimerScore:
    '''class that adds score every 2 seconds and can save it to a file'''
    scores_data = []

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
            self.begin_count = current_time

    def add_points(self, points):
        '''manually adds points to player'''
        self.score += points

    def save_scores(self, player_name):
        '''writes the scores, plus the new score to pickle file'''
        today = date.today()
        cur_date = today.strftime("%m/%d/%Y")
        seconds = math.floor(
            (pygame.time.get_ticks() - self.start_time) / 1000)
        self.scores_data.append([self.score, player_name, seconds, cur_date])
        self.scores_data.sort(key=lambda x: x[0])
        self.scores_data.sort(reverse=True)
        with open('game_data.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(self.scores_data, f, pickle.HIGHEST_PROTOCOL)

    def populate_scores(self):
        '''populates the game with the players to beat'''
        scores_list = [[6000, "Jacob", 310, "6/25/2021"], [1200, "John", 150, "5/20/2021"],
                       [555, "Niko", 55, "6/24/2021"], [300,
                                                        "Dave", 20, "2/12/2021"],
                       [150, "Jack", 15, "1/11/2021"]]
        with open('game_data.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(scores_list, f, pickle.HIGHEST_PROTOCOL)

    def import_scores(self):
        '''takes the scores in from the pickle file'''
        with open('game_data.pickle', 'rb') as fh:
            self.scores_data = pickle.load(fh)

    def wait_time(self):
        '''waits a certain amount of time before completing the scene'''
        if pygame.time.get_ticks() >= self.begin_count + self.tick_time_ms:
            return False
        return True
