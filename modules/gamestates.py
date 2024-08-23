from abc import ABC, abstractmethod
from typing import override
from game import Game


class GameState(ABC):
    def __init__(self, game:Game) -> None:
        self.game = game

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def onmousedown(self):
        pass

class Pause(GameState):
    pass

class Settings(GameState):
    pass




class Restart(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.MSG = transform_scale(MSG_IMG,MSG_SIZE)

    @override
    def update(self):
        return super().update()

    @override
    def onmousedown(self):
        return super().onmousedown()




class Play(GameState):
    @override
    def update(self):
        self.game.bird.update()
        self.game.pipe.update()
        self.game.base.move()

        # collision of bird with pipe
        if self.game.bird.rect.colliderect(self.game.pipe.top_rectangle()) or self.game.bird.rect.colliderect(self.game.pipe.bottom_rectangle()):
            self.game.gamestate = Restart(self.game)
        
        # collision of bird with sky or base
        if not self.game.bird.height < self.game.bird.rect.bottom < self.game.base.y:
            self.game.gamestate = Restart(self.game)

    @override
    def onmousedown(self):
        self.game.bird.flap()

