import pygame
from Board import Board
from constants import *
from datetime import datetime
import os
import csv
import numpy as np


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.ROWS, self.COLS = ROWS, COLS
        self.RECT_WIDTH, self.RECT_HEIGHT = RECT_WIDTH, RECT_HEIGHT
        self.OUTLINE_THICKNESS = OUTLINE_THICKNESS
        
        pygame.font.init()
        self.FONT = pygame.font.SysFont(None, 90)

        self.OUTLINE_COLOR = OUTLINE_COLOR
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        self.FONT_COLOR = FONT_COLOR

        self.BOXES_COLORS = BOXES_COLORS
        self.DIGITS = {i: 2**i for i in range(1, 10)} # STORED FOR MAKING IT MORE EFFICENT

        self.TIME_SLEEP = TIME_SLEEP
        self.START_TIME = datetime.now().strftime("%y%m%d%H%M%S")
        self.LOGS_FNAME = LOGS_FNAME

        self.weights = weights

        self.board = Board()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.logs = []
    
    def save_logs(self):
        if not os.path.isdir(self.LOGS_FNAME):
            os.mkdir(self.LOGS_FNAME)
        
        with open(os.path.join(self.LOGS_FNAME, self.START_TIME), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.logs)
    
    def draw_background(self):
        self.window.fill(self.BACKGROUND_COLOR)

    def draw_grid(self):
        for row in range(1, self.ROWS):
            y = row * self.RECT_HEIGHT
            pygame.draw.line(self.window, self.OUTLINE_COLOR, (0, y), (WIDTH, y), self.OUTLINE_THICKNESS)
        for col in range(1, COLS):
            x = col * RECT_WIDTH
            pygame.draw.line(self.window, self.OUTLINE_COLOR, (x, 0), (x, self.HEIGHT), self.OUTLINE_THICKNESS)

        pygame.draw.rect(self.window, self.OUTLINE_COLOR, (0, 0, self.WIDTH, self.HEIGHT), self.OUTLINE_THICKNESS)
    
    def draw_box(self, row, col):
        n = self.board.grid[row, col]
        if n!=0:
            color = self.BOXES_COLORS[n]
            x = col * self.RECT_WIDTH
            y = row * self.RECT_HEIGHT
                
            pygame.draw.rect(self.window, color, (x, y, self.RECT_WIDTH, self.RECT_HEIGHT))
            text = FONT.render(str(2**(n)), 1, self.FONT_COLOR)
            self.window.blit(
                text, 
                (
                    x + (self.RECT_WIDTH - text.get_width())//2,
                    y + (self.RECT_HEIGHT - text.get_height())//2
                ),
            )
    
    def refresh_window(self):
        self.draw_background()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.draw_box(row, col)
        self.draw_grid()
        pygame.display.update()

    def read_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        return 'up'
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        return 'down'
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        return 'left'
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        return 'right'
        return None

    def run(self):
        while (not self.board.game_over) and (not self.board.win):
            self.refresh_window()
            action = self.read_action()
            if action in self.board.possible_moves:
                self.board.move(action)
                self.board.add_2()
                self.board.check_possible_moves()
                self.board.is_game_over()
                self.board.is_win()
                self.logs.append([self.board.grid.reshape(-1), action, self.board.reward(10000, 8, self.weights)])
                print(self.board.grid)
                pygame.time.wait(self.TIME_SLEEP)
        self.save_logs()


def reward(punctuation: int, win: bool, game_over: bool, grid: np.array, max_punctuation: int, max_zeros: int, weights: dict, logarithmic_punctuation: bool=True):
    total_reward = 0.

    if win:
        total_reward += weights.get('win', 0)
    elif game_over:
        total_reward += weights.get('game over', 0)
    
    vals, freqs = np.unique(grid, return_counts=True)
    num_zeros = freqs[vals==0].sum()
    avg_freq = freqs[vals!=0].mean()

    if logarithmic_punctuation:
        total_reward += min(np.log(punctuation+1)/np.log(max_punctuation), 1) * weights.get('punctuation', 0)
    else:
        total_reward += min(punctuation/max_punctuation, 1) * weights.get('punctuation', 0)
    
    total_reward += min(num_zeros/max_zeros, 1) * weights.get('zeros', 0)
    total_reward += min(2 - avg_freq, 1) * weights.get('distribution', 0)

    return total_reward


game = Game()
game.run()