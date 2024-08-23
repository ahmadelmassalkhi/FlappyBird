import random
import pygame
from game import Game
from utils import Utils


class Pipe(object):

    def __init__(self, x, game:Game):
        self.game = game

        # pipe information
        self.VELOCITY = 5 * game.relative_percent
        self.GAP = 300 * game.relative_percent
        self.x = x

        # pipe height
        self.minHeight = 100 * game.relative_percent
        self.maxHeight = self.minHeight + self.GAP

        # set default color
        self.setcolor_green()
        self.generate_height()
    
    
    def setcolor_green(self):
        self.BOTTOM_PIPE_IMAGE = self.IMAGE = pygame.transform.scale(
            Utils.load_and_convert('./Images/pipe-green.png'), Utils.re_size((104, 640), self.game.relative_percent))
        self.TOP_PIPE_IMAGE = pygame.transform.flip(self.BOTTOM_PIPE_IMAGE, False, True)

    def setcolor_red(self):
        self.BOTTOM_PIPE_IMAGE = self.IMAGE = pygame.transform.scale(
            Utils.load_and_convert('./Images/pipe-red.png'), Utils.re_size((104, 640), self.game.relative_percent))
        self.TOP_PIPE_IMAGE = pygame.transform.flip(self.BOTTOM_PIPE_IMAGE, False, True)


    def update(self):
        # move pipe
        self.x -= self.VELOCITY
        
        # score
        if self.x + self.IMAGE.get_width() < 0:
            self.game.score += 1
            self.x = self.game.screen.WIDTH
            self.generate_height()
        
        # draw to game's screen
        self.game.screen.draw(self.BOTTOM_PIPE_IMAGE, self.bottom_rectangle())
        self.game.screen.draw(self.TOP_PIPE_IMAGE, self.top_rectangle())


    def bottom_rectangle(self):
        centerX = self.x + self.IMAGE.get_width()//2
        centerY = (self.height - self.IMAGE.get_height() // 2) + self.IMAGE.get_height() + self.GAP
        return self.BOTTOM_PIPE_IMAGE.get_rect(center=(centerX, centerY))


    def top_rectangle(self):
        centerX = self.x + self.IMAGE.get_width()//2
        centerY = (self.height - self.IMAGE.get_height() // 2)
        return self.TOP_PIPE_IMAGE.get_rect(center=(centerX, centerY))
    

    def generate_height(self):
        self.height = random.randrange(
            int(self.minHeight), int(self.game.base.y - (self.maxHeight)))
    
