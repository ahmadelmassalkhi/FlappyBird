import json
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import gamestates as gamestates
from typing import Tuple


class Game:

    def __init__(self) -> None:

        # configurations
        self.relative_percent = .75
        self.fps = 120
        self.gravity = 1/4
        self.score = self.highscore = 0

        # load
        self.load_sounds()
        self.load_fonts()

        # screen
        from screen import Screen
        self.screen = Screen(self)

        # objects on screen
        from Entities.bird import Bird
        from Entities.base import Base
        from Entities.pipe import Pipe
        self.bird = Bird(self)
        self.base = Base(self)
        self.pipe = Pipe(self)


        # gamestate & mode
        self.setmode_day()
        self.state = gamestates.Restart(self)

        # other
        self.clock = pygame.time.Clock()



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.score > self.highscore:
                        data = {'High score': self.score}
                        with open('storage.txt', 'w') as storage_file:
                            json.dump(data, storage_file)
                    pygame.quit()
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    self.state.onmousedown(event)
            
            self.screen.draw(self.background, (0,0))
            self.state.update()
            self.base.draw()

            # update display at fps
            pygame.display.update()
            self.clock.tick(self.fps)


    def setmode_night(self):
        self.bird.setcolor_red()
        self.pipe.setcolor_red()
        self.background = self.load_image('Images/background-night.png', (self.screen.WIDTH, self.screen.HEIGHT))

    def setmode_day(self):
        self.bird.setcolor_yellow()
        self.pipe.setcolor_green()
        self.background = self.load_image('Images/background-day.png', (self.screen.WIDTH, self.screen.HEIGHT))
        

    def load_highscore(self):
        try:
            with open('storage.txt') as storage_file:
                data = json.load(storage_file)
        except:
            print("Storage not created yet!")

    def load_fonts(self):
        self.game_font = pygame.font.Font('04B_19.ttf',40)
        self.settings_font = pygame.font.Font('04B_19.ttf',25)

    def load_sounds(self):
        self.flap_sound = pygame.mixer.Sound('./Sounds/wing.wav')
        self.death_sound = pygame.mixer.Sound('./Sounds/hit.wav')
        self.score_sound = pygame.mixer.Sound('./Sounds/point.wav')


    def load_image(self, path:str, size:Tuple[float,float], rescale:bool=False):
        if rescale: 
            return pygame.transform.scale(pygame.image.load(path).convert_alpha(), self.rescale(size))
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

    def rescale(self, size:Tuple[float, float]):
        return (size[0] * self.relative_percent,
                size[1] * self.relative_percent)

    def flip_image(self, image:pygame.Surface, flip_x:bool, flip_y:bool):
        return pygame.transform.flip(image, flip_x, flip_y)
    




if __name__ == '__main__':
    pygame.init()
    Game().run()