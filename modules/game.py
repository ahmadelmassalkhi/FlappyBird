import json
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import gamestates as gamestates
from utils import Utils


class Game:
    def __init__(self) -> None:

        # configurations
        self.relative_percent = .75
        self.fps = 60
        self.gravity = 1/4
        self.score = self.highscore = 0

        # load
        self.load_sounds()
        self.load_fonts()

        # screen
        from screen import Screen
        self.screen = Screen(self)

        # objects on screen
        from bird import Bird
        from base import Base
        from pipe import Pipe
        self.bird = Bird(100 * self.relative_percent, self.screen.HEIGHT // 2, self)
        self.base = Base(0, self)
        self.pipe = Pipe(self.screen.WIDTH, self)


        # gamestate & mode
        self.setmode_day()
        self.gamestate = gamestates.Play(self)

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
                    self.gamestate.onmousedown()
            
            self.screen.draw(self.background, (0,0))
            self.gamestate.update()
            self.base.draw()

            # update display at fps
            pygame.display.update()
            self.clock.tick(self.fps)


    def setmode_night(self):
        self.bird.setcolor_red()
        self.pipe.setcolor_red()
        self.background = Utils.transform_scale(Utils.load_and_convert('Images/background-night.png'),
                                                (self.screen.WIDTH, self.screen.HEIGHT))

    def setmode_day(self):
        self.bird.setcolor_yellow()
        self.pipe.setcolor_green()
        self.background = Utils.transform_scale(Utils.load_and_convert('Images/background-day.png'),
                                         (self.screen.WIDTH, self.screen.HEIGHT))
        
    
    def load_fonts(self):
        game_font = pygame.font.Font('04B_19.ttf',40)
        settings_font = pygame.font.Font('04B_19.ttf',25)

    def load_sounds(self):
        flap_sound = pygame.mixer.Sound('./Sounds/wing.wav')
        death_sound = pygame.mixer.Sound('./Sounds/hit.wav')
        score_sound = pygame.mixer.Sound('./Sounds/point.wav')
        
    def load_highscore(self):
        try:
            with open('storage.txt') as storage_file:
                data = json.load(storage_file)
        except:
            print("Storage not created yet!")


if __name__ == '__main__':
    pygame.init()
    Game().run()