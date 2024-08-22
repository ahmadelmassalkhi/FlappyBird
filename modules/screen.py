import pygame
from utils import *


class Screen:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT) = re_size((576, 1024))
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.BG_IMG = pygame.transform.scale(load_and_convert(
            'Images/background-day.png'), self.SCREEN_SIZE)
