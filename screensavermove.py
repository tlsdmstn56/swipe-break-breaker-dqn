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

seconds = 45 * 60
ticks = 0

#Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MINT = (183, 255, 236)
BLUE = (0, 131, 249)
DARK_MINT = (0, 103, 111)

# Make a player
player = [100, 100, 25, 25]
player_vx = 0
player_vy = 0
player_speed = 5

block1 = [100, 100, 50, 25, 5]
block2 = [250, 100, 50, 25, 5]
block3 = [400, 100, 50, 25, 5]

blocks = [block1, block2, block3]

# Game loop
done = False

while not done:
    # Event processing (react to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    


    # Game logic (Check for collisions, update points, etc.)
    ticks += 1
    if ticks == 60:
        player_vx += 5
        player_vy += 5


    ''' move the player in horizontal direction'''
    player[0] += player_vx


    ''' here is where you should resolve player collisions with screen edges '''
    LEFT = player[0]
    RIGHT = player[0] + player[2]

    if LEFT < 0:
        player_vx *= -1
    elif RIGHT > WIDTH:
        player_vx *= -1

    
    for b in blocks:
        block_rect = b[:4] 
        if intersects.rect_rect(player, b):
            if player_vx > 0:
                player[0] = b[0] - player[2]
            else:
                player[0] = b[0] + b[2]
            player_vx *= -1
            b[4] -= 1

    ''' move the player in vertical direction '''
    player[1] += player_vy

    TOP = player[1]
    BOTTOM = player[1] + player[3]

    if TOP < 0:
        player_vy *= -1
    elif BOTTOM > HEIGHT:
        player_vy *= -1


    for b in blocks:
        if intersects.rect_rect(player, b):
            if player_vy > 0:
                player[1] = b[1] - player[3]
            else:
                player[1] = b[1] + b[3]
            player_vy *= -1 
            b[4] -= 1 
  
    


    #Drawing code (describe picture. it isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.ellipse(screen, BLUE, player)
    for b in blocks:
        block_rect = b[:4]
        if b[4] < 1:
            pygame.draw.rect(screen, RED, block_rect)
        else:
            pygame.draw.rect(screen, DARK_MINT, block_rect)


    #update screen(actually draw the picture in the window.)
    pygame.display.flip()


    # limit refresh rate of game loop
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()


    
            

