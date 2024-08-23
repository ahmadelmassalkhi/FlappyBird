import pygame
from game import Game
from utils import Utils




class Base:

    def __init__(self, x, game:Game) -> None:
        self.game = game
        self.image = pygame.transform.scale(Utils.load_and_convert('./Images/base.png'), 
                                            Utils.re_size((672, 224), game.relative_percent))


        # coordinates
        self.x = x
        self.y = 900 * game.relative_percent
        
        # dimensions
        self.SIZE = (self.WIDTH, self.HEIGHT) = Utils.re_size((672, 224), game.relative_percent)


    def move(self):
        self.x -= 5 * self.game.relative_percent
        if self.x < - self.game.screen.WIDTH:
            self.x = 0
    
    def draw(self):
        self.game.screen.draw(self.image, (self.x, self.y))
        self.game.screen.draw(self.image, (self.x + self.game.screen.WIDTH, self.y))
