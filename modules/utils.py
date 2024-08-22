import pygame
from settings import Settings


def re_size(x):
    return (int(x[0] * Settings().RELATIVE_PERCENT),
            int(x[1] * Settings().RELATIVE_PERCENT))


def load_and_convert(path):
    return pygame.image.load(path).convert_alpha()
