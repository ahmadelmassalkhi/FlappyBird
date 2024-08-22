import pygame
from utils import *
from screen import Screen
from settings import Settings


class Base:
    IMAGE = pygame.transform.scale(
        load_and_convert('Images/base.png'), re_size((672, 224)))
    Y = 900 * Settings().RELATIVE_PERCENT

    def __init__(self, x) -> None:
        self.x = x

    def update(self):
        self.x -= 5 * Settings().RELATIVE_PERCENT
        if self.x < -Screen().WIDTH:
            self.x = 0
        
        # draw it
        Screen().SCREEN.blit(Base.IMAGE, (self.x, Base.Y))
        Screen().SCREEN.blit(Base.IMAGE, (self.x + Screen().WIDTH, Base.Y))
