from modules.utils import *
from modules.settings import Settings
from modules.screen import Screen
from modules.pipe import Pipe
from modules.bird import Bird
from modules.base import Base
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import neat
import os
import random
import json
import pickle



class Game:
    def __init__(self) -> None:
        self.score = self.highscore = 0
        self.clock = pygame.time.Clock()
        self.running = self.canScore = True

        # interactive objects
        self.base = Base(0)
        self.pipe = Pipe(Screen().WIDTH)
        self.bird = Bird(100 * Settings().RELATIVE_PERCENT, Screen().HEIGHT//2)

    def run(self):
        while self.running:
            # draw background
            Screen().SCREEN.blit(Screen().BG_IMG, (0, 0))

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.score > self.highscore:
                        data = {'High score': self.score}
                        with open('storage.txt', 'w') as storage_file:
                            json.dump(data, storage_file)
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.bird.flap()

            # update interactive objects
            self.bird.update()
            self.pipe.update()
            self.base.update()

            # Scoring mechanics
            if self.bird.x-5 < self.pipe.x < self.bird.x+5 and self.canScore:
                self.score += 1
                self.canScore = False
            if self.pipe.x < 0:
                self.canScore = True
            
            pygame.display.update()
            self.clock.tick(Settings().FPS)

    def load_highscore(self):
        try:
            with open('storage.txt', 'r') as storage_file:
                data = json.load(storage_file)
                self.highscore = data['High score']
        except:
            self.highscore = 0

    def check_collision(self):
        if self.bird.rect.colliderect(self.pipe.bottom_rectangle()) or self.bird.rect.colliderect(self.pipe.top_rectangle()):
            pass
        if not Bird.IMAGES[0].get_height() < self.bird.rect.bottom < self.base.y:
            pass



def game(genomes, config):
    base = Base(0)
    score = 0

    while running and len(birds):
        Screen().SCREEN.blit(Screen().BG_IMG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(prev_score, score)
                if score > prev_score:
                    data = {'High score': score}
                    with open('storage.txt', 'w') as storage_file:
                        json.dump(data, storage_file)
                    with open('winner.pickle', 'wb') as winner_file:
                        pickle.dump(genomes[0][1], winner_file)
                pygame.quit()
                quit()

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            output = nets[birds.index(bird)].activate(
                (bird.y, abs(bird.y - pipe.topRectY), abs(bird.y - pipe.bottomRectY)))
            if output[0] > 0.5:
                bird.jump()

        # Drawing objects
        for bird in birds:
            bird.draw()
        pipe.draw()

        # Scoring mechanics
        if bird.x-5 < pipe.x < bird.x+5 and canScore:
            score += 1
            canScore = False
            for genome in ge:
                genome.fitness += 5
        if pipe.x < 0:
            canScore = True

        # Collision check
        pipes = pipe.rects()
        for bird in birds:
            if bird.rect.colliderect(pipes[0]) or bird.rect.colliderect(pipes[1]):
                decrease_fitness(ge, nets, bird, birds)
        for bird in birds:
            if not Bird.IMAGES[0].get_height() < bird.rect.bottom < base.y:
                decrease_fitness(ge, nets, bird, birds)

        if not len(birds):
            pipe.x = Screen().WIDTH

        # Base stuff
        base.move()
        base.draw()

        # score
        score_label = STAT_FONT.render(
            "Score: " + str(score), 1, (255, 255, 255))
        Screen().SCREEN.blit(score_label, (Screen().WIDTH - score_label.get_width() - 15, 10))

        # generations
        gens_label = STAT_FONT.render(
            "Gens: " + str(gen-1), 1, (255, 255, 255))
        Screen().SCREEN.blit(gens_label, (10, 10))

        # alive
        alive_label = STAT_FONT.render(
            "Alive: " + str(len(birds)), 1, (255, 255, 255))
        Screen().SCREEN.blit(alive_label, (10, 50))

        # Updating display
        pygame.display.update()
        clock.tick(Settings().FPS)


def decrease_fitness(ge, nets, bird, birds):
    ge[birds.index(bird)].fitness -= 1
    nets.pop(birds.index(bird))
    ge.pop(birds.index(bird))
    birds.pop(birds.index(bird))


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(game, 50)
    print('\nBest genome:\n{!s}'.format(winner))

    if score > prev_score:
        data = {'High score': score}
        with open('storage.txt', 'w') as storage_file:
            json.dump(data, storage_file)
        with open('winner.pickle', 'wb') as winner_file:
            pickle.dump(winner, winner_file)


def replay_genome(config_path, genome_path="winner.pickle"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    game(genomes, config)


if __name__ == '__main__':
    replay_winner = 0
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    try:
        with open('storage.txt', 'r') as storage_file:
            data = json.load(storage_file)
            prev_score = data['High score']
    except:
        prev_score = 0

    if replay_winner:
        replay_genome(config_path)
    else:
        run(config_path)
