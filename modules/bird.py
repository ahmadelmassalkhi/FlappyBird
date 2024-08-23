import pygame
from utils import Utils
from game import Game


class Bird(object):

    def __init__(self, x, y, game:Game):
        self.game = game # needed to adjust bird's movement to obey game's settings

        # bird's information
        self.x = x
        self.y = y
        self.vel = 0
        self.width, self.height = Utils.re_size((68,48), game.relative_percent)

        # bird's look
        self.setcolor_yellow()
        self.imgIndex = 0
        self.img = self.IMAGS[self.imgIndex]


    def flap(self):
        self.vel = 0
        self.vel -= 11 * self.game.relative_percent
        self.y += self.vel


    def update(self):
        self.vel += self.game.gravity
        self.y += self.vel

        # animate
        if self.vel == 0:
            self.imgIndex = 0
        elif self.vel > 0:
            self.imgIndex = 2
        else:
            self.imgIndex = 1

        # update image & rectangle
        self.img = pygame.transform.rotozoom(self.IMAGS[self.imgIndex],-self.vel * 3,1)
        self.rect = self.get_rectangle()

        # draw bird to game's screen
        self.game.screen.draw(self.img, self.rect)

    
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
        RED_DOWNFLAP_IMG = Utils.load_and_convert('./Images/redbird-midflap.png')
        RED_MIDFLAP_IMG = Utils.load_and_convert('./Images/redbird-upflap.png')
        RED_UPFLAP_IMG = Utils.load_and_convert('./Images/redbird-downflap.png')
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
