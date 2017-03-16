#this is the constant in process game, every time you complete a new task save
#it as a new game ex. game1
#
# March 16, 2017
#

import pygame
import intersects


# Initialze game engine
pygame.init()

# open file
file = open('highScore.txt', 'r+')
content = file.read()


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
MINT2 = (0, 164, 176)
MINT3 = (0, 226, 244)
MINT4 = (113, 244, 255)
MINT5 = (134, 254, 255)
randco = (35, 54, 62)

#font
font = pygame.font.Font(None, 48)
font2 = pygame.font.Font(None, 35)

# Make a player
player = [400, 775, 25, 25]
player_vx = 0
player_vy = 0
player_speed = 5

playing = False
win = False
lose = False
game_over = False

x_value = -5

score = 0

direction = "Left"

blocks = []

for y in range(100, 300, 25):
    for x in range(0, WIDTH - 50, 75):
        b = [x, y, 75, 25, 5]
        blocks.append(b)

powerups = []

for y in range(50, 100, 50):
    for x in range(25, WIDTH, 75):
        p = [x, y, 25, 25, 1]
        powerups.append(p)

print(powerups)

# Game loop
done = False

while not done:
    # Event processing (react to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if game_over == False:
                if playing == False:
                    if event.key == pygame.K_LEFT:
                        x_value = -5
                        direction = "Left"
                    elif event.key == pygame.K_RIGHT:
                        x_value = 5
                        direction = "Right"
                    if event.key == pygame.K_SPACE:
                        player_vx = x_value
                        player_vy = -5
                        playing = True
                        score += 1
                    

    


    # Game logic (Check for collisions, update points, etc.)



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

    for p in powerups:
        if intersects.rect_rect(player, p):
            if player_vx > 0:
                p[4] -= 1
            else:
                p[4] -= 1
                

    ''' move the player in vertical direction '''
    player[1] += player_vy

    TOP = player[1]
    BOTTOM = player[1] + player[3]

    if TOP < 0:
        player_vy *= -1
    elif BOTTOM > HEIGHT:
        player_vy = 0
        player_vx = 0
        if playing == True:
            for b in blocks:
                if b[1] <= HEIGHT - 50:
                    b[1]+= 25
                    if b[1] >= HEIGHT - 25:
                        lose = True
                    

        playing = False
        


    for b in blocks:
        if intersects.rect_rect(player, b):
            if player_vy > 0:
                player[1] = b[1] - player[3]
            else:
                player[1] = b[1] + b[3]
            player_vy *= -1 
            b[4] -= 1 

    for p in powerups:
        if intersects.rect_rect(player, p):
            p[4] -= 1

    
    ''' get blocks '''
    blocks = [b for b in blocks if b[4] > 0]
    powerups = [p for p in powerups if p[4] > 0]

    if len(blocks) == 0:
        win = True
        playing = True

    if score >= 101:
        lose = True
        playing = True

    if lose == True:
        game_over = True

    if win == True:
        with open('highScore.txt', 'r+') as f:
            if str(score) < content:
                file.write(score)

    
    #Drawing code (describe picture. it isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.ellipse(screen, BLUE, player)

    LorR = font.render("Direction: " + str(direction), 1, WHITE)
    screen.blit(LorR, [400, 0])
    
    for b in blocks:
        block_rect = b[:4]
        if b[4] == 5:
            pygame.draw.rect(screen, DARK_MINT, block_rect)
            bhits = font2.render(str(b[4]), 1, WHITE)
            screen.blit(bhits, [b[0] + 30, b[1]])
        if b[4] == 4:
            pygame.draw.rect(screen, MINT2, block_rect)
            bhits = font2.render(str(b[4]), 1, WHITE)
            screen.blit(bhits, [b[0] + 30, b[1]])
        if b[4] == 3:
            pygame.draw.rect(screen, MINT3, block_rect)
            bhits = font2.render(str(b[4]), 1, WHITE)
            screen.blit(bhits, [b[0] + 30, b[1]])
        if b[4] == 2:
            pygame.draw.rect(screen, MINT4, block_rect)
            bhits = font2.render(str(b[4]), 1, WHITE)
            screen.blit(bhits, [b[0] + 30, b[1]])
        if b[4] == 1:
            pygame.draw.rect(screen, MINT5, block_rect)
            bhits = font2.render(str(b[4]), 1, WHITE)
            screen.blit(bhits, [b[0] + 30, b[1]])

    for p in powerups:
        powerup_rect = p[:4]
        if p[4] >= 1:
            pygame.draw.rect(screen, randco,  powerup_rect)
                                 

    if win == True:
        winner = font.render("You Win!", 1, WHITE)
        screen.blit(winner, [400, 300])

    if lose == True:
        loser = font.render("You Lose!", 1, WHITE)
        screen.blit(loser, [400, 300])

    scoring = font.render(str(score), 1, WHITE)
    screen.blit(scoring, [0, 0])

    highscore = font.render("High Score: " + content, 1, WHITE)
    screen.blit(highscore, [700, 0])
    #update screen(actually draw the picture in the window.)
    pygame.display.flip()


    # limit refresh rate of game loop
    clock.tick(refresh_rate)


# close window and quit
pygame.quit()


    
            

