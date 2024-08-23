import pygame
from utils import Utils
from typing import Union, Tuple
from game import Game


class Screen:
    
    # singleton design pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self, game:Game) -> None:
        self.WIDTH, self.HEIGHT = Utils.re_size((576,1024), game.relative_percent)
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))


    def draw(self, surface:pygame.Surface, 
             dest:Union[pygame.Rect, Tuple[float, float]]):
        self.WINDOW.blit(surface, dest)
