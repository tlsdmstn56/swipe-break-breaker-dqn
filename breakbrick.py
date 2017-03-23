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
RED = (255, 4, 20)
WHITE = (255, 255, 255)
PINK = (254, 199, 204)
LIGHT = (232, 237, 223)
BLUE2 = (8, 65, 92)

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (115, 255, 0)
BLUE = (0, 167, 225)
DARK_MINT = (0, 103, 111)
MINT2 = (0, 164, 176)
MINT3 = (0, 226, 244)
MINT4 = (113, 244, 255)
MINT5 = (134, 254, 255)
randco = (35, 54, 62)

# Font //////////////////////////////////////////////////////////////////////////
font = pygame.font.Font(None, 48)
font2 = pygame.font.Font(None, 35)

# Stuff to set outside game loop ///////////////////////////////////////////////
playing = False
win = False
lose = False
game_over = False
speed = 7
score = 0

# Make a Player ////////////////////////////////////////////////////////////////

class Ball:

    def __init__(self, x, y, width, height, ball_vx, ball_vy, ball_speed):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ball_vx = ball_vx
        self.ball_vy = ball_vy
        self.ball_speed = ball_speed

    def draw(self):
        pygame.draw.ellipse(screen, BLUE, [self.x, self.y, self.width, self.height])


# Make Blocks //////////////////////////////////////////////////////////////////

class Block:

    def __init__(self, x, y, width, height, hits):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hits = hits

    def draw(self):
        pygame.draw.rect(screen, RED, [self.x, self.y, self.width, self.height])
        bhits = font2.render(str(self.hits), 1, WHITE)
        screen.blit(bhits, [self.x + 30, self.y])

        
# velocity for balls////////////////////////////////////////////////////////////

def get_vel(bx, by, mx, my, speed):
    a = mx - bx
    b = my - by
    c = math.sqrt((a**2) + (b**2))

    vx = int(speed) * (a/c)
    vy = int(speed) * (b/c)

    return vx, vy

# List of Blocks ///////////////////////////////////////////////////////////////

blocks = []

blocks.append(Block(5, 51, 99, 34, 2))
blocks.append(Block(105, 51, 99, 34, 2))
blocks.append(Block(205, 51, 99, 34, 2))

# List of Balls ////////////////////////////////////////////////////////////////

balls = []

balls.append(Ball(500, 725, 25, 25, 0, 0, 5))

# Game Loop ////////////////////////////////////////////////////////////////////
done = False

while not done:
    # Event processing /////////////////////////////////////////////////////////
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if game_over == False:
            if playing == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    #bx, by = 

                    ball_vx, ball_vy = get_vel(bx, by, mx, my, speed)
                    playing = True
                    score += 1

    # Game Logic ///////////////////////////////////////////////////////////////

    ''' move the ball in horizontal direction '''
    

    ''' resolves player collusiions with screen edges '''
    '''LEFT = ball[0]
    RIGHT = ball[0] + ball[2]

    if LEFT < 0:
        ball_vx *= -1
    elif RIGHT > WIDTH:
        ball_vx *= -1'''

    # Drawing code /////////////////////////////////////////////////////////////
    screen.fill(LIGHT)

    pygame.draw.rect(screen, BLUE2, [0, 0, WIDTH, 50])
    pygame.draw.rect(screen, BLUE2, [0, HEIGHT - 50, WIDTH, 50])
    pygame.draw.rect(screen, GREEN, [0, 50, WIDTH, 5])
    pygame.draw.rect(screen, GREEN, [WIDTH - 5, 50, 5, HEIGHT - 110])

    for b in balls:
        b.draw()

    for b in blocks:
        b.draw()
    
    #update screen ///////////////////////////////////////////////////////////
    pygame.display.flip()

    # Limit refresh rate of game loop //////////////////////////////////////////
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
    
             
        
