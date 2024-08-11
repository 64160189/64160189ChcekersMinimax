import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgba
RED = (217,95,95,255)
WHITE = (242,242,242,255)
BLACK = (0, 0, 0)
BLUE = (46,110,166,255)
GREY = (130,121,118)
GREEN = (219,242,39,255)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (32, 32))
