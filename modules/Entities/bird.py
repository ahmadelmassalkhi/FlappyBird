import pygame
from utils import Utils
from game import Game
from Entity import GameEntity
from typing import override



class Bird(GameEntity):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # bird's information
        self.width, self.height = Utils.re_size((68,48), game.relative_percent)

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
        YELLOW_DOWNFLAP_IMG = Utils.load_and_convert('./Images/yellowbird-downflap.png')
        YELLOW_MIDFLAP_IMG = Utils.load_and_convert('./Images/yellowbird-midflap.png')
        YELLOW_UPFLAP_IMG = Utils.load_and_convert('./Images/yellowbird-upflap.png')
        self.IMAGS = [Utils.transform_scale(YELLOW_DOWNFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(YELLOW_MIDFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(YELLOW_UPFLAP_IMG, (self.width, self.height))]
        
    def setcolor_red(self):
        RED_DOWNFLAP_IMG = Utils.load_and_convert('./Images/redbird-downflap.png')
        RED_MIDFLAP_IMG = Utils.load_and_convert('./Images/redbird-midflap.png')
        RED_UPFLAP_IMG = Utils.load_and_convert('./Images/redbird-upflap.png')
        self.IMAGS = [Utils.transform_scale(RED_DOWNFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(RED_MIDFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(RED_UPFLAP_IMG, (self.width, self.height))]

    def setcolor_blue(self):
        BLUE_DOWNFLAP_IMG = Utils.load_and_convert('./Images/bluebird-downflap.png')
        BLUE_MIDFLAP_IMG = Utils.load_and_convert('./Images/bluebird-midflap.png')
        BLUE_UPFLAP_IMG = Utils.load_and_convert('./Images/bluebird-upflap.png')
        self.IMAGS = [Utils.transform_scale(BLUE_DOWNFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(BLUE_MIDFLAP_IMG, (self.width, self.height)),
                      Utils.transform_scale(BLUE_UPFLAP_IMG, (self.width, self.height))]
