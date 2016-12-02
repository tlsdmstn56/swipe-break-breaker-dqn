#this is the screen saver (math) function of my game
#
# December 02, 2016
#

import pygame
import intersects

# Initialze game engine
pygame.init()

# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Swipe Break Screen Saver"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

#Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Make a player
player = [200, 150, 25, 25]
player_vx = 0
player_vy = 0
player_speed = 5

# Game loop
done = False

while not done:
    # Event processing (react to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    


    # Game logic (Check for collisions, update points, etc.)
    ''' move the player in horizontal direction'''
    player[0] += player_vx

    ''' move the player in vertical direction '''
    player[1] += player_vy

    ''' here is where you should resolve player collisions with screen edges '''
    TOP = player[1]
    BOTTOM = player[1] + player[3]
    LEFT = player[0]
    RIGHT = player[0] + player[2]

    if TOP <0:
        player[1] = 0
    elif BOTTOM > HEIGHT:
        player[1] = HEIGHT - player[3]

    if LEFT < 0:
        player[0] = 0
    elif RIGHT > WIDTH:
        player[0] = WIDTH - player[2]


    #Drawing code (describe picture. it isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, player)


    #update screen(actually draw the picture in the window.)
    pygame.display.flip()


    # limit refresh rate of game loop
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()


    
            

