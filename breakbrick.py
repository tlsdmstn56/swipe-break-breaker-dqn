#This will be the code that I turn in for the create performance task
#This code will be similar to the original one that I have but will
#include functions and more organization
#
# March 20, 2017
#

import pygame
import intersects
import math

# Initialize game engine ///////////////////////////////////////////////////////
pygame.init()

# Open file ////////////////////////////////////////////////////////////////////
file = open('highScore.txt', 'r+')
content = file.read()

# Window ///////////////////////////////////////////////////////////////////////
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Brick Breaker"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer ////////////////////////////////////////////////////////////////////////
clock = pygame.time.Clock()
refresh_rate = 60

# Colors ///////////////////////////////////////////////////////////////////////
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 131, 249)
DARK_MINT = (0, 103, 111)
MINT2 = (0, 164, 176)
MINT3 = (0, 226, 244)
MINT4 = (113, 244, 255)
MINT5 = (134, 254, 255)
randco = (35, 54, 62)

# Font //////////////////////////////////////////////////////////////////////////
font = pygame.font.Font(None, 48)
font2 = pygame.font.Font(None, 35)

# Make a Player ////////////////////////////////////////////////////////////////

class 
