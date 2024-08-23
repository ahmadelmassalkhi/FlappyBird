import pygame
from game import Game
from Entity import GameEntity
from typing import override



class Bird(GameEntity):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # bird's information
        self.width, self.height = game.rescale((68, 48))

        # bird's look
        self.setcolor_yellow()
        self.imgIndex = 0
        self.img = self.IMAGS[self.imgIndex]
        self.reset_coordinates()


    @override
    def reset_coordinates(self):
        self.vel = 0
        self.x = 100 * self.game.relative_percent
        self.y = self.game.screen.HEIGHT/2 - self.img.get_height()/2

    @override
    def move(self):
        self.vel += self.game.gravity
        self.y += self.vel

        # animate
        if self.vel == 0: # midflap
            self.imgIndex = 1
        elif self.vel > 0: # downflap
            self.imgIndex = 2
        else: # upflap
            self.imgIndex = 0

        # update image & rectangle
        self.img = pygame.transform.rotozoom(self.IMAGS[self.imgIndex],-self.vel * 3,1)
        self.rect = self.get_rectangle()
    
    @override
    def draw(self):
        self.game.screen.draw(self.img, self.rect)


    def flap(self):
        self.vel = 0
        self.vel -= 11 * self.game.relative_percent
        self.y += self.vel
        
    def get_rectangle(self):
        return self.img.get_rect(center = (self.x, self.y))
    

    def setcolor_yellow(self):
        self.IMAGS = [
            self.game.load_image('./Images/yellowbird-downflap.png', (self.width, self.height)),
            self.game.load_image('./Images/yellowbird-midflap.png', (self.width, self.height)),
            self.game.load_image('./Images/yellowbird-upflap.png', (self.width, self.height))]
        
    def setcolor_red(self):
        self.IMAGS = [
            self.game.load_image('./Images/redbird-downflap.png', (self.width, self.height)),
            self.game.load_image('./Images/redbird-midflap.png', (self.width, self.height)),
            self.game.load_image('./Images/redbird-upflap.png', (self.width, self.height))]

    def setcolor_blue(self):
        self.IMAGS = [
            self.game.load_image('./Images/bluebird-downflap.png', (self.width, self.height)),
            self.game.load_image('./Images/bluebird-midflap.png', (self.width, self.height)),
            self.game.load_image('./Images/bluebird-upflap.png', (self.width, self.height))]
