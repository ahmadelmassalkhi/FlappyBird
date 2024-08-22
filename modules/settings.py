import pygame

pygame.init()


# initialize fonts
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)


class Settings:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.replay_winner = 0
        self.GRAVITY = 1/4
        self.FPS = 1200
        self.RELATIVE_PERCENT = .75
