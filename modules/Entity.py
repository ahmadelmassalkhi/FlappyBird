from abc import ABC, abstractmethod
from game import Game



class GameEntity(ABC):
    def __init__(self, game:Game) -> None:
        self.game = game

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def reset_coordinates(self):
        pass

    