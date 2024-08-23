import random
import pygame
from game import Game
from utils import Utils
from Entity import GameEntity
from typing import override

class Pipe(GameEntity):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # pipe information
        self.VELOCITY = 5 * game.relative_percent
        self.GAP = 300 * game.relative_percent

        # pipe height
        self.minHeight = 100 * game.relative_percent
        self.maxHeight = self.minHeight + self.GAP

        # set default color & location
        self.setcolor_green()
        self.reset_coordinates()
    
    @override
    def move(self):
        # move pipe
        self.x -= self.VELOCITY
        
        # score
        if self.x + self.IMAGE.get_width() < 0:
            self.game.score += 1
            self.reset_coordinates()
            
    @override
    def draw(self):
        self.game.screen.draw(self.BOTTOM_PIPE_IMAGE, self.bottom_rectangle())
        self.game.screen.draw(self.TOP_PIPE_IMAGE, self.top_rectangle())

    @override
    def reset_coordinates(self):
        self.x = self.game.screen.WIDTH
        self.height = random.randrange(
            int(self.minHeight), int(self.game.base.y - (self.maxHeight)))

        
    def bottom_rectangle(self):
        centerX = self.x + self.IMAGE.get_width()//2
        centerY = (self.height - self.IMAGE.get_height() // 2) + self.IMAGE.get_height() + self.GAP
        return self.BOTTOM_PIPE_IMAGE.get_rect(center=(centerX, centerY))

    def top_rectangle(self):
        centerX = self.x + self.IMAGE.get_width()//2
        centerY = (self.height - self.IMAGE.get_height() // 2)
        return self.TOP_PIPE_IMAGE.get_rect(center=(centerX, centerY))
    

    def setcolor_green(self):
        self.BOTTOM_PIPE_IMAGE = self.IMAGE = pygame.transform.scale(
            Utils.load_and_convert('./Images/pipe-green.png'), Utils.re_size((104, 640), self.game.relative_percent))
        self.TOP_PIPE_IMAGE = pygame.transform.flip(self.BOTTOM_PIPE_IMAGE, False, True)

    def setcolor_red(self):
        self.BOTTOM_PIPE_IMAGE = self.IMAGE = pygame.transform.scale(
            Utils.load_and_convert('./Images/pipe-red.png'), Utils.re_size((104, 640), self.game.relative_percent))
        self.TOP_PIPE_IMAGE = pygame.transform.flip(self.BOTTOM_PIPE_IMAGE, False, True)
