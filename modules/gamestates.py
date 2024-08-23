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
        self.image = self.game.load_image('Images/message_getready.png', (368, 534), True)

    def draw_message(self):
        self.game.screen.draw(self.image,
                              (self.game.screen.WIDTH/2 - self.image.get_width()/2, 
                               self.game.screen.HEIGHT/2 - self.image.get_height()/2))

    @override
    def update(self):
        self.draw_message()

    @override
    def onmousedown(self):
        self.game.pipe.reset_coordinates()
        self.game.bird.reset_coordinates()
        self.game.state = Play(self.game)
    



class GameOver(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.image = self.game.load_image('Images/gameover.png', (384, 84), True)

    def draw_message(self):
        self.game.screen.draw(self.image,
                              (self.game.screen.WIDTH/2 - self.image.get_width()/2, 
                               self.game.screen.HEIGHT/2 - self.image.get_height()/2))

    @override
    def update(self):
        self.game.bird.draw()
        self.game.pipe.draw()
        self.draw_message()

    @override
    def onmousedown(self):
        self.game.state = Restart(self.game)




class Play(GameState):
    @override
    def update(self):
        # move
        self.game.bird.move()
        self.game.pipe.move()
        self.game.base.move()

        # draw
        self.game.bird.draw()
        self.game.pipe.draw()
        self.game.base.draw()

        # collision of bird with pipe
        if self.game.bird.rect.colliderect(self.game.pipe.top_rectangle()) or self.game.bird.rect.colliderect(self.game.pipe.bottom_rectangle()):
            self.game.state = GameOver(self.game)
        
        # collision of bird with sky or base
        if not self.game.bird.height < self.game.bird.rect.bottom < self.game.base.y:
            self.game.state = GameOver(self.game)

    @override
    def onmousedown(self):
        self.game.bird.flap()

