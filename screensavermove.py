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

block = [300, 200, 400, 400, 5]

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

    block_rect = block[:4]
    
    if intersects.rect_rect(player, block_rect):
        if player_vx > 0:
            player[0] = block_rect[0] - player[2]
        else:
            player[0] = block_rect[0] + block_rect[2]
        player_vx *= -1
        block[4] -= 1

    ''' move the player in vertical direction '''
    player[1] += player_vy

    TOP = player[1]
    BOTTOM = player[1] + player[3]

    if TOP < 0:
        player_vy *= -1
    elif BOTTOM > HEIGHT:
        player_vy *= -1


    if intersects.rect_rect(player, block):
        if player_vy > 0:
            player[1] = block[1] - player[3]
        else:
            player[1] = block[1] + block[3]
        player_vy *= -1 
 
  
    


    #Drawing code (describe picture. it isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.ellipse(screen, BLUE, player)

    if block[4] < 1:
        pygame.draw.rect(screen, RED, block)
    else:
        pygame.draw.rect(screen, DARK_MINT, block)


    #update screen(actually draw the picture in the window.)
    pygame.display.flip()


    # limit refresh rate of game loop
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()


    
            

