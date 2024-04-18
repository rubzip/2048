from collections import defaultdict
import pygame


WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4

RECT_WIDTH = WIDTH // ROWS
RECT_HEIGHT = HEIGHT // COLS
pygame.font.init()
OUTLINE_THICKNESS = 10
FONT = pygame.font.SysFont(None, 90)

OUTLINE_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

BOXES_COLORS = defaultdict(lambda : (236, 202, 80))
for i in range(1, 10):
    BOXES_COLORS[2**i] = COLORS[i-1]
