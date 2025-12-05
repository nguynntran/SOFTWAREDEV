import pygame

class Cons:
    # Board
    WIDTH, HEIGHT = 800, 800
    ROWS, COLS = 8, 8
    SQUARE_SIZE = WIDTH // COLS

    # Color (RGB mode)
    WHITE = (255, 255, 255) #Hightlight
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    SELECT = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

    # Character
    EMP = 0
    WOLF = 1
    SHEEP = 2