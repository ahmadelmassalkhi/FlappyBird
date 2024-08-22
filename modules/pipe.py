import pygame
import random
from settings import Settings
from utils import *
from screen import Screen
from base import Base


class Pipe(object):
    TOP_PIPE_IMAGE = pygame.transform.scale(
        load_and_convert('Images/pipe.png'), re_size((104, 640)))
    BOTTOM_PIPE_IMAGE = pygame.transform.flip(TOP_PIPE_IMAGE, False, True)
    VELOCITY = 5 * Settings().RELATIVE_PERCENT
    GAP = 300*Settings().RELATIVE_PERCENT

    def __init__(self, x):
        self.x = x

        self.minHeight = 100 * Settings().RELATIVE_PERCENT
        self.maxHeight = self.minHeight + Pipe.GAP
        self.height = random.randrange(
            int(self.minHeight), int(Base.Y-(self.maxHeight)))

        self.topRectY = self.height - Pipe.IMAGE.get_height()//2
        self.bottomRectY = self.topRectY + Pipe.IMAGE.get_height() + Pipe.GAP

    def update(self):
        self.x -= Pipe.VELOCITY
        if self.x+Pipe.IMAGE.get_width() < 0:
            global pipe, score
            pipe = Pipe(Screen().WIDTH)
            self.x = Screen().WIDTH
            score += 1
        # draw
        Screen().SCREEN.blit(Pipe.BOTTOM_PIPE_IMAGE, self.bottom_rectangle())
        Screen().SCREEN.blit(Pipe.TOP_PIPE_IMAGE, self.top_rectangle())


    def bottom_rectangle(self):
        return Pipe.BOTTOM_PIPE_IMAGE.get_rect(
            center=(self.x+Pipe.IMAGE.get_width()//2, self.bottomRectY))

    def top_rectangle(self):
        return Pipe.TOP_PIPE_IMAGE.get_rect(
            center=(self.x + Pipe.IMAGE.get_width()//2, self.topRectY))
