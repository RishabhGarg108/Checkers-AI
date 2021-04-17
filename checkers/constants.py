import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS

class Color:
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  GREY = (128, 128, 128)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)


# CROWN = pygame.transform.scale(pygame.image.load('assets/king.png'), (44, 25))