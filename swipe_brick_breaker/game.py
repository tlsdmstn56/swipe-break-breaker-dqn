# from . import intersects
from .utils import remove_collided_objects, get_vel
from .configs import Config
from .colors import BLUE2, LIGHT, BLACK, RED, WHITE
from .objects import Powerup, Block, Ball, Rect
import pygame

import random
from enum import Enum

class Grid:

    def __init__(self):
        super().__init__()

    def get_game_state(self):
        pass

    def remove_dead(self):
        ''' this removes the blocks when all of the hits have been made '''
        to_remove = list(filter(lambda b : b.get_hits() > 0, self))
        self.clear()
        self.extend(to_remove)

class Game:

    class Mode(Enum):
        WAITING_USER_INPUT = 1
        PLAY = 2
        GAMEOVER = 3

    def __init__(self, config: Config):
        self.config = config

        # basic game config
        screen_size = (config.window_width, config.window_height)
        self.screen = pygame.display.set_mode(screen_size)
        self.width = config.window_width
        self.height = config.window_height
        pygame.display.set_caption(config.title)

        # board size
        self.board_upper = self.config.header_height + self.config.header_footer_line_height # noqa: E501
        self.board_lower = self.config.window_width - self.config.footer_height - self.config.header_footer_line_height # noqa: E501
        self.board_height = self.board_lower - self.board_upper
        self.board_width = self.config.window_height

        # FPS
        self.clock = pygame.time.Clock()
        self.fps = config.fps

        # set size of blocks
        self.block_width = self.board_width/self.config.grid_width
        self.block_height = self.board_height/self.config.grid_height
        Rect.set_size(
            self.block_width, self.block_height, self.config.block_border_width)

        # list of block
        self.blocks = []

        # starts with one ball
        Ball.set_radius(self.config.ball_radius)
        self.balls = []
        self.balls.append(Ball(self.width/2, 715, 0))

        # score and the number of blocks in the new row
        self.score = 1

        # list of items
        self.powerups = []

        # game mode
        self.stage = self.Mode.WAITING_USER_INPUT

        # fonts
        self.font = pygame.font.Font(None, 48)
        self.font2 = pygame.font.Font(None, 35)
        self.font3 = pygame.font.Font(None, 70)
        self.font4 = pygame.font.Font(None, 100)

        # colors
        self.color_high_score = pygame.Color(255, 30, 30)
        self.color_low_score = pygame.Color(255, 170, 170)


    def get_color_by_score(self, current_score:int):
        assert current_score <= self.score
        ratio = current_score / self.score
        return self.color_low_score.lerp(self.color_high_score, ratio)


    def init_blocks(self):
        blocks = []
        for i in range(self.config.grid_width):
            blocks.append(Block(i * self.block_width, self.block_height, 1))
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
        width = self.config.window_width
        height = self.config.window_height

        header_height = self.config.header_height
        footer_height = self.config.footer_height
        header_footer_line_height = self.config.header_footer_line_height

        header_rect = [0, 0, width, header_height]
        footer_rect = [0, height - footer_height, width, footer_height]
        header_line_rect = [0, header_height, width, header_footer_line_height]
        footer_line_rect = [
            0, height - footer_height - header_footer_line_height, 
                width, header_footer_line_height]
        pygame.draw.rect(self.screen, BLUE2, header_rect)
        pygame.draw.rect(self.screen, BLUE2, footer_rect)
        pygame.draw.rect(self.screen, BLACK, header_line_rect)
        pygame.draw.rect(self.screen, BLACK, footer_line_rect)

        scoring = self.font.render(f"Score: {self.score}", 1, WHITE)
        self.screen.blit(scoring, [15, 7])

        ballCount = self.font.render(f"Ball Count: {len(self.balls)}", 1, WHITE)
        ballCount_rect = ballCount.get_rect()
        w = (width - ballCount_rect.width)- 15
        self.screen.blit(ballCount, [w, 7])

        name = self.font3.render("Click to break bricks", 1, WHITE)
        name_rect = name.get_bounding_rect()
        w = (width - name_rect.width)/2 
        self.screen.blit(name, [w, height - 50])

    def all_stopped(self):
        ''' This allows for the next click to be made '''
        for b in self.balls:
            if b.vx != 0 or b.vy != 0:
                return False

        return True

    def prepare_new_row(self):
        if self.score < 25:
            min_block = 2
            max_block = 3
        elif self.score < 50:
            min_block = 3
            max_block = 4
        elif self.score < 75:
            min_block = 3
            max_block = 5
        else:
            min_block = 4
            max_block = self.config.grid_width
        
        k = random.sample(range(min_block, max_block+1), 1)
        index = random.sample(range(self.config.grid_width), k[0])
        
        row_y = self.block_height+self.board_upper
        # always generate 1 item
        self.powerups.append(
            Powerup(index[0] * self.block_width, row_y, 1)
        )

        self.blocks.extend([
            Block(i * self.block_width, row_y, self.score)
            for i in index[1:]
        ])

    def update(self):
        if self.stage != self.Mode.PLAY:
            return

        for b in self.blocks:
            b.update(self)
        for p in self.powerups:
            p.update(self)
        self.prepare_new_row()
        begin = self.balls[0].x
        for b in self.balls:
            b.x = begin

        self.stage = self.Mode.WAITING_USER_INPUT

        if len(self.blocks) > 0:
            first = self.blocks[0].y
            for b in self.blocks:
                if b.y >= first:
                    first = b.y
            if first >= self.height - 120:
                self.stage = self.Mode.GAMEOVER

        if len(self.powerups) > 0:
            for p in self.powerups:
                if p.y >= self.height - 120:
                    self.powerups.remove(p)

        self.score += 1

    def draw(self, showline, mouse_pos):
        self.draw_board()

        for b in self.balls:
            b.draw(self.screen)

        for b in self.blocks:
            b.draw(self)

        for p in self.powerups:
            p.draw(self.screen)

        if showline:
            assert mouse_pos is not None
            m_x, m_y = mouse_pos
            line_rect = [self.balls[0].x + 10, self.balls[0].y + 10]
            pygame.draw.line(self.screen, RED, line_rect, mouse_pos, 1)

    def run(self):

        # Game Loop
        done = False

        # setup initial board
        self.prepare_new_row()

        while not done:
            # check input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if self.stage == self.Mode.WAITING_USER_INPUT:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mx, my = pygame.mouse.get_pos()
                        count = 0
                        for b in self.balls:
                            b.vx, b.vy = get_vel(b.x, b.y, mx, my, self.config.ball_speed) # noqa: E501
                            b.delay = count
                            count += 5

                        self.stage = self.Mode.PLAY

            pressed = pygame.mouse.get_pressed()
            if pressed:
                mouse_pos = pygame.mouse.get_pos()
            else:
                mouse_pos = None

            # move balls
            if self.stage == self.Mode.PLAY:
                for b in self.balls:
                    if b.delay <= 0:
                        b.update(self)
                    b.delay -= 1

            remove_collided_objects(self.blocks)
            remove_collided_objects(self.powerups)

            if self.all_stopped():
                self.update()
                

            # draw
            self.draw(pressed[0], mouse_pos)
            
            if self.stage == self.Mode.GAMEOVER:
                self.game_over()

            # update display
            pygame.display.flip()

            # Limit refresh rate of game loop
            self.clock.tick(self.fps)