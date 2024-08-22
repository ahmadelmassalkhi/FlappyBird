import os
import pygame
from utils import *
from settings import Settings
from screen import Screen


class Bird(object):
    IMAGES = [pygame.transform.scale(pygame.image.load(os.path.join(
        "Images", "bird" + str(x) + ".png")), re_size((68, 48))) for x in range(1, 4)]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.imgIndex = 0
        self.img = Bird.IMAGES[self.imgIndex]
        self.rect = self.img.get_rect(center=(x, self.y))

    def flap(self):
        self.vel = 0
        self.vel -= 11 * Settings().RELATIVE_PERCENT
        self.y += self.vel

    def update(self):
        self.vel += Settings().GRAVITY
        self.y += self.vel
        self.rotate_n_animate()
        Screen().SCREEN.blit(self.img, self.rect)

    def rotate_n_animate(self):
        if not self.vel:
            self.imgIndex = 0
        elif self.vel > 0:
            self.imgIndex = 2
        else:
            self.imgIndex = 1
        self.img = Bird.IMAGES[self.imgIndex]
        self.img = pygame.transform.rotozoom(self.img, -self.vel * 3, 1)
        self.rect = self.img.get_rect(center=(self.x, self.y))
