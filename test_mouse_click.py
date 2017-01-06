#this is the test program for mouse click
#
# January 04, 2017
#

import pygame
import math

#initialze game engine
pygame.init()

# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Mouse Click Test"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors

# Font

#player
player = [45, 23]

# Game loop
done = False
mpos= 0
slope = 0
rise = 0
run = 0

while not done:
    # Event processing (react to key presses, mouse clicks, etc.)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            rise = (mpos[1] - player[1]) 
            run = (mpos[0] - player[0])
          

    # Game Logic
   

    # Drawing Code
    print(mpos)
    print(str(rise) + "/" + str(run))

    #update screen
    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()

    

    

    
