import pygame
from .utils import intersects
from .colors import GREEN, RED, WHITE


class BreakableMixin:

    def __init__(self, hits:int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hits = hits

    def is_breakable(self):
        return self.hits <= 0

class Rect:

    width = None
    height = None
    border_width = None

    @classmethod
    def set_size(cls, width, height, border_width):
        cls.width = width
        cls.height = height
        cls.border_width = border_width

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y

    def get_rect(self):
        return [self.x, self.y, self.width, self.height]
    
    def get_draw_rect(self):
        rect = self.get_rect()
        rect[0] += self.border_width
        rect[1] += self.border_width
        rect[2] -= 2* self.border_width
        rect[3] -= 2* self.border_width
        return rect

class Ball:

    radius = None

    @classmethod
    def set_radius(cls, r):
        cls.radius = r

    def __init__(self, x, y, delay):
        self.x = x
        self.y = y
        self.delay = delay
        self.vx = 0
        self.vy = 0

    def get_rect(self):
        return [self.x, self.y, self.radius , self.radius]

    def update(self, game):
        # move ball in x direction
        if self.delay <= 0:
            self.x += self.vx

        # resolve x edge detection
        if self.x < 0:
            self.vx *= -1

        if self.x > game.width - self.radius:
            self.vx *= -1

        # resolve x block collisions
        for b in game.blocks:
            if intersects(self.get_rect(), b.get_rect()):
                if self.vx > 0:
                    self.x = b.x - self.radius
                else:
                    self.x = b.x + b.width
                self.vx *= -1
                b.hits -= 1

        # resolve x powerup collisions
        for p in game.powerups:
            if intersects(self.get_rect(), p.get_rect()):
                p.hits -= 1
                game.balls.append(Ball(game.width/2, 715, 50)) 

        # move ball in y direction
        if self.delay <= 0:
            self.y += self.vy

        # resolve y edge detection
        if self.y < 60:
            self.vy *= -1

        if self.y > game.height - 85:
            self.vy  = 0
            self.vx  = 0
            self.y = game.height - 85

        # resolve y block collisions
        for b in game.blocks:
            if intersects(self.get_rect(), b.get_rect()):
                if self.vy > 0:
                    self.y = b.y - self.radius
                else:
                    self.y = b.y + b.height
                self.vy *= -1
                b.hits -= 1

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.get_rect())

class Block(BreakableMixin, Rect):

    def __init__(self, x, y, hits):
        super().__init__(x=x, y=y, hits=hits)

    def update(self, game):
        blocks = game.blocks
        height = game.config.window_height

        if len(blocks) > 0:
            first = blocks[0].y
            for b in blocks:
                if b.y >= first:
                    first = b.y

            if first <= height - 120:
                self.y += game.block_height

    def draw(self, game):
        color = game.get_color_by_score(self.hits)
        pygame.draw.rect(game.screen, color, self.get_draw_rect())
        bhits = game.font2.render(f'{self.hits}', 1, WHITE)
        font_w = (self.width - bhits.get_width()) / 2
        font_h = (self.height - bhits.get_height()) / 2
        game.screen.blit(bhits, [self.x + font_w, self.y + font_h])


class Powerup(BreakableMixin, Rect):

    def __init__(self, x, y, hits):
        super().__init__(x=x, y=y, hits=hits)

    def update(self, game):
        self.y += game.block_height

    def draw(self, screen, *args, **kwargs):
        pygame.draw.rect(screen, GREEN, self.get_draw_rect())