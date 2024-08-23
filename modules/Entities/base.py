import pygame
from game import Game
from Entity import GameEntity
from typing import override


class Base(GameEntity):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.image = self.game.load_image('./Images/base.png', (672, 224), True)
        self.reset_coordinates()
        self.SIZE = (self.WIDTH, self.HEIGHT) = self.game.rescale((672, 224))

    @override
    def move(self):
        self.x -= 5 * self.game.relative_percent
        if self.x < - self.game.screen.WIDTH:
            self.x = 0
    
    @override
    def draw(self):
        self.game.screen.draw(self.image, (self.x, self.y))
        self.game.screen.draw(self.image, (self.x + self.game.screen.WIDTH, self.y))

    @override
    def reset_coordinates(self):
        self.x = 0
        self.y = 900 * self.game.relative_percent
