import pygame
import intersects
import math
import random
import json
import pathlib
import argparse
from enum import Enum

from swipe_brick_breaker.configs import *
from swipe_brick_breaker.utils import *

class Ball:

    width = None
    height = None

    @classmethod
    def set_size(cls, width, height):
        cls.width = width
        cls.height = height

    def __init__(self, x, y, delay):
        self.x = x
        self.y = y
        self.delay = delay
        self.vx = 0
        self.vy = 0
        
    def get_rect(self):
        return [self.x, self.y, self.width, self.height]
    
    def update(self, balls, blocks, powerups):
        # move ball in x direction 
        if self.delay <= 0:
            self.x += self.vx

        # resolve x edge detection
        if self.x < 0:
            self.vx *= -1

        if self.x > WIDTH - self.width:
            self.vx *= -1

        # resolve x block collisions
        for b in blocks:
            if intersects(self.get_rect(), b.get_rect()):
                if self.vx > 0:
                    self.x = b.x - self.width
                else:
                    self.x = b.x + b.width
                self.vx *= -1
                b.hits -= 1

        # resolve x powerup collisions
        for p in powerups:
            if intersects(self.get_rect(), p.get_rect()):
                p.hits -= 1
                balls.append(Ball(WIDTH/2, 715, 50)) #come back to solve powerup problem
                
        # move ball in y direction
        if self.delay <= 0:
            self.y += self.vy

        # resolve y edge detection
        if self.y < 60:
            self.vy *= -1

        if self.y > HEIGHT - 85:
            self.vy  = 0
            self.vx  = 0
            self.y = HEIGHT - 85

        # resolve y block collisions
        for b in blocks:
            if intersects(self.get_rect(), b.get_rect()):
                if self.vy > 0:
                    self.y = b.y - self.height
                else:
                    self.y = b.y + b.height
                self.vy *= -1
                b.hits -= 1
                
    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, [self.x, self.y, self.width, self.height])

# class Block(pygame.sprite.Sprite):

#     def __init__(self, color, width, height):
#        super().__init__()

#        # Create an image of the block, and fill it with a color.
#        # This could also be an image loaded from the disk.
#        self.image = pygame.Surface([width, height])
#        self.image.fill(BLUE)

#        # Fetch the rectangle object that has the dimensions of the image
#        # Update the position of this object by setting the values of rect.x and rect.y
#        self.rect = self.image.get_rect()

class BreakableRect:
    
    width = None
    height = None

    @classmethod
    def set_size(cls, width, height):
        cls.width = width
        cls.height = height

    def __init__(self, x, y, hits):
        self.x = x
        self.y = y
        self.hits = hits

    def get_rect(self):
        return [self.x, self.y, self.width, self.height]

class Block(BreakableRect):    

    def __init__(self, x, y, hits):
        super().__init__(x, y, hits)

    def update(self, blocks, *args, **kwargs):
        if len(blocks) > 0:
            first = blocks[0].y
            for b in blocks:
                if b.y >= first:
                    first = b.y
        
            if first <= HEIGHT - 120:
                self.y += 40

    def draw(self, screen, font, *args, **kwargs):
        pygame.draw.rect(screen, BLUE, self.get_rect())
        bhits = font.render(str(self.hits), 1, WHITE)
        linex = self.width / 2 - bhits.get_width() / 2
        screen.blit(bhits, [self.x + linex, self.y + 5])


class Powerup(BreakableRect):

    def __init__(self, x, y, hits):
        super().__init__(x, y, hits)

    def update(self, *args, **kwargs):
        self.y += 40
 
    def draw(self, screen, *args, **kwargs):
        pygame.draw.rect(screen, GREEN, [self.x, self.y, self.width, self.height])

class Grid:

    def __init__(self):
        super().__init__()

    def get_game_state(self):
        pass

    def remove_dead(self):
        ''' this removes the blocks when all of the hits have been made '''
        to_remove = list(filter(lambda b : b.hits > 0, self))
        self.clear()
        self.extend(to_remove) 

class Game:

    class Mode(Enum):
        NOT_STARTED = 1
        PLAY = 2
        GAMEOVER = 3

    def __init__(self, fps=DEFAULT_FPS):
        # basic game config
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)

        # FPS
        self.clock = pygame.time.Clock()
        self.fps = fps

        # set size of blocks
        BreakableRect.set_size(BLOCK_WIDTH, BLOCK_HEIGHT)

        # list of block 
        self.blocks = self.init_blocks()

        # starts with one ball
        Ball.set_size(BALL_RADIUS, BALL_RADIUS)
        self.balls = []
        self.balls.append(Ball(WIDTH/2, 715, 0))

        # score and the number of blocks in the new row
        self.score = 0

        # list of items
        self.powerups = []

        # game mode
        self.stage = self.Mode.NOT_STARTED

        # fonts
        self.font = pygame.font.Font(None, 48)
        self.font2 = pygame.font.Font(None, 35)
        self.font3 = pygame.font.Font(None, 70)
        self.font4 = pygame.font.Font(None, 100)

    
    def init_blocks(self):
        blocks = []
        blocks.append(Block(0, 100, 1))
        blocks.append(Block(105, 100, 1))
        blocks.append(Block(210, 100, 1))
        blocks.append(Block(315, 100, 1))
        blocks.append(Block(420, 100, 1))
        blocks.append(Block(525, 100, 1))
        blocks.append(Block(630, 100, 1))
        blocks.append(Block(735, 100, 1))
        return blocks

    def game_over(self):
        pygame.draw.rect(self.screen, WHITE, [105, 100, 625, 600])
        pygame.draw.rect(self.screen, BLACK, [105, 100, 625, 600], 10)
        pygame.draw.rect(self.screen, RED, [120, 230, 585, 20])
        if len(self.blocks) > 0:
            lose = self.font4.render("GAME OVER", 1, BLACK)
            self.screen.blit(lose, [200, 150])
        finalScore = self.font3.render(f"FINAL SCORE: {self.score}", 1, BLACK)
        self.screen.blit(finalScore, [200, 280])
        finalCount = self.font3.render(f"FINAL BALL COUNT: {len(self.balls)}", 1, BLACK)
        self.screen.blit(finalCount, [160, 360])

    def draw_board(self):
        self.screen.fill(LIGHT)

        pygame.draw.rect(self.screen, BLUE2, [0, 0, WIDTH, 50])
        pygame.draw.rect(self.screen, BLUE2, [0, HEIGHT - 50, WIDTH, 50])
        pygame.draw.rect(self.screen, BLACK, [0, 50, WIDTH, 10])
        pygame.draw.rect(self.screen, BLACK, [0, HEIGHT - 60, WIDTH, 10])

        scoring = self.font.render(f"Score: {self.score}", 1, WHITE)
        self.screen.blit(scoring, [5, 7])

        ballCount = self.font.render(f"Ball Count: {len(self.balls)}", 1, WHITE)
        self.screen.blit(ballCount, [300, 7])

        name = self.font3.render("Click Brick Break", 1, WHITE)
        self.screen.blit(name, [200, HEIGHT - 50])

    def all_stopped(self):
        ''' This allows for the next click to be made '''
        for b in self.balls:
            if b.vx != 0 or b.vy != 0:
                return False

        return True    

    
    def get_new_row(self):
        ''' drops a new row of blocks at the end of each turn '''
        b1 = Block(0, 100, int(self.score))
        b2 = Block(105, 100, int(self.score))
        b3 = Block(210, 100, int(self.score))
        b4 = Block(315, 100, int(self.score))
        b5 = Block(420, 100, int(self.score))
        b6 = Block(525, 100, int(self.score))
        b7 = Block(630, 100, int(self.score))
        b8 = Block(735, 100, int(self.score))

        row = [b1, b2, b4, b5, b7, b8]

        rlist = [ row[i] for i in random.sample(range(len(row)), 4) ]

        self.blocks.append(rlist[0])
        self.blocks.append(rlist[1])
        self.blocks.append(rlist[2])

    def get_new_powerup(self):

        p3 = Powerup(210, 100, 1)
        p6 = Powerup(525, 100, 1)

        row =  [p3, p6]

        num = random.randint(0, 1)

        rlist = [ row[i] for i in random.sample(range(len(row)), num) ]

        if num > 0:
            self.powerups.append(rlist[0])

    def run(self):

        # Game Loop
        done = False

        while not done:
            # check input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if self.stage == self.Mode.NOT_STARTED:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mx, my = pygame.mouse.get_pos()
                        count = 0
                        for b in self.balls:
                            b.vx, b.vy = get_vel(b.x, b.y, mx, my, BALL_SPEED)
                            b.delay = count
                            count += 5
                            
                        self.stage = self.Mode.PLAY
                        self.score += 1

            pressed = pygame.mouse.get_pressed()
            if pressed:
                m_x, m_y = pygame.mouse.get_pos()
                            

            # Game Logic

            showline = pressed[0]
                
            # move balls
            if self.stage == self.Mode.PLAY:
                for b in self.balls:
                    if b.delay <= 0:
                        b.update(self.balls, self.blocks, self.powerups)
                    b.delay -= 1

            remove_collided_objects(self.blocks)
            remove_collided_objects(self.powerups)
            
            if self.all_stopped():
                if self.stage == self.Mode.PLAY:
                    for b in self.blocks:
                        b.update(self.blocks)
                    for p in self.powerups:
                        p.update()
                    self.get_new_row()
                    self.get_new_powerup()
                    begin = self.balls[0].x
                    for b in self.balls:
                        b.x = begin
                    
                    self.stage = self.Mode.NOT_STARTED

                    if len(self.blocks) > 0:
                        first = self.blocks[0].y
                        for b in self.blocks:
                            if b.y >= first:
                                first = b.y
                        if first >= HEIGHT - 120:
                            stage = self.Mode.GAMEOVER

                    if len(self.powerups) > 0:
                        for p in self.powerups:
                            if p.y >= HEIGHT - 120:
                                self.powerups.remove(p)

            # draw
            self.draw_board()
            
            for b in self.balls:
                b.draw(self.screen)

            for b in self.blocks:
                b.draw(self.screen, self.font2)

            for p in self.powerups:
                p.draw(self.screen)

            if showline:
                pygame.draw.line(self.screen, RED, [self.balls[0].x + 10, self.balls[0].y + 10], [m_x, m_y,], 1)

            if self.stage == self.Mode.GAMEOVER:
                self.game_over()    
            
            # update display
            pygame.display.flip()

            # Limit refresh rate of game loop
            self.clock.tick(self.fps)

        

def main(args):
    pygame.init()
    game = Game(args.fps)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=float, default=DEFAULT_FPS)
    args = parser.parse_args()
    main(args)
        
