import pygame, neat, os, random, json, pickle
pygame.font.init()  # init font
pygame.init()


'''
    y_n = input('Replay best genome? (y/n) ')
    if y_n.lower()=='y':
        replay_winner = True
    else:
        replay_winner = False
'''
replay_winner = 0

    
def re_size(x):
    size = (int(x[0]*RELATIVE_PERCENT),int(x[1]*RELATIVE_PERCENT))
    return size


def load_and_convert(path):
    img = pygame.image.load(path).convert_alpha()
    return img


STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

GRAVITY = 1/4
FPS = 1200
RELATIVE_PERCENT=.75
BASE_Y = 900*RELATIVE_PERCENT
SCREEN_SIZE = (WIDTH,HEIGHT) = re_size((576,1024))
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

PIPE_IMG = pygame.transform.scale(load_and_convert('Images/pipe.png'),re_size((104,640)))
BG_IMG = pygame.transform.scale(load_and_convert('Images/background-day.png'), SCREEN_SIZE)
BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("Images","bird" + str(x) + ".png")),re_size((68,48))) for x in range(1,4)]
BASE_IMG = pygame.transform.scale(load_and_convert('Images/base.png'),re_size((672,224)))

class Bird(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 0
        self.imgIndex = 0
        self.img = BIRD_IMGS[self.imgIndex]
        self.rect = self.img.get_rect(center = (x,self.y))
    
    def jump(self):
        self.vel = 0
        self.vel -= 11*RELATIVE_PERCENT
        self.y += self.vel

    def draw(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rotate_n_animate()
        SCREEN.blit(self.img,self.rect)

    def rotate_n_animate(self):
        if not self.vel:
            self.imgIndex = 0
        elif self.vel>0:
            self.imgIndex = 2
        else:
            self.imgIndex = 1
        self.img = BIRD_IMGS[self.imgIndex]
        self.img = pygame.transform.rotozoom(self.img,-self.vel * 3,1)
        self.rect = self.img.get_rect(center = (self.x,self.y))
        

PIPES = [PIPE_IMG,pygame.transform.flip(PIPE_IMG, False, True)]
PIPES_HEIGHT = [value*RELATIVE_PERCENT for value in [400,600,800]]
score = 0
PIPE_VEL = 0
GAP = 0

class Pipe(object):

    global PIPE_VEL, GAP
    PIPE_VEL = 5*RELATIVE_PERCENT
    GAP = 300*RELATIVE_PERCENT

    def __init__(self,x):
        self.x = x
        self.minHeight = 100*RELATIVE_PERCENT
        self.maxHeight = self.minHeight + GAP
        self.height = random.randrange(int(self.minHeight), int(BASE_Y-(self.maxHeight)))
        self.topRectY = self.height - PIPE_IMG.get_height()//2
        self.bottomRectY = self.topRectY + PIPE_IMG.get_height() + GAP
        self.rects()
        
        
    def draw(self):
        self.move()
        SCREEN.blit(PIPES[0],self.rects()[0])
        SCREEN.blit(PIPES[1],self.rects()[1])

    def move(self):
        self.x -= PIPE_VEL
        if self.x+PIPE_IMG.get_width()<0:
            global pipe,score
            pipe = Pipe(WIDTH)
            self.x = WIDTH
            score+=1


    def rects(self):
        self.bottomRect = PIPES[0].get_rect(center = (self.x+PIPE_IMG.get_width()//2,self.bottomRectY))
        self.topRect = PIPES[1].get_rect(center = (self.x+PIPE_IMG.get_width()//2,self.topRectY))
        return self.bottomRect,self.topRect
    
    
pipe = Pipe(WIDTH)
gen = 0
birds =  []
bird = Bird(100*RELATIVE_PERCENT,HEIGHT//2)

def game(genomes,config):
    global gen
    gen+=1

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(100*RELATIVE_PERCENT,HEIGHT//2))
        ge.append(genome)
    
    baseX = score = 0
    canScore = running =True
    
    while running and len(birds):
        SCREEN.blit(BG_IMG,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(prev_score,score)
                if score>prev_score:
                    data = {'High score': score}
                    with open('storage.txt','w') as storage_file:
                        json.dump(data,storage_file)
                    with open('winner.pickle','wb') as winner_file:
                        pickle.dump(genomes[0][1],winner_file)
                pygame.quit()
                quit()

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipe.topRectY), abs(bird.y - pipe.bottomRectY)))
            if output[0] > 0.5:
                bird.jump()
            

        #Drawing objects
        for bird in birds:
            bird.draw()
        pipe.draw()


        #Scoring mechanics
        if bird.x-5<pipe.x<bird.x+5 and canScore:
            score+=1
            canScore = False
            for genome in ge:
                genome.fitness += 5
        if pipe.x<0:
            canScore=True

        #Collision check
        pipes = pipe.rects()
        for bird in birds:
            if bird.rect.colliderect(pipes[0]) or bird.rect.colliderect(pipes[1]):
                decrease_fitness(ge,nets,bird,birds)
        for bird in birds:
            if not BIRD_IMGS[0].get_height()<bird.rect.bottom<BASE_Y:
                decrease_fitness(ge,nets,bird,birds)
        
        if not len(birds):
            pipe.x = WIDTH   
            

        #Base stuff
        baseX -= 5*RELATIVE_PERCENT
        if baseX<-WIDTH:
            baseX = 0
        SCREEN.blit(BASE_IMG,(baseX,BASE_Y))
        SCREEN.blit(BASE_IMG,(baseX+WIDTH,BASE_Y))

        # score
        score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
        SCREEN.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))

        # generations
        gens_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
        SCREEN.blit(gens_label, (10, 10))

        # alive
        alive_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
        SCREEN.blit(alive_label, (10, 50))

        #Updating display
        pygame.display.update()
        clock.tick(FPS)

def decrease_fitness(ge,nets,bird,birds):
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

    if score>prev_score:
        data = {'High score': score}
        with open('storage.txt','w') as storage_file:
            json.dump(data,storage_file)
        with open('winner.pickle','wb') as winner_file:
            pickle.dump(winner,winner_file)

def replay_genome(config_path, genome_path="winner.pickle"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    game(genomes,config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    try:
        with open('storage.txt','r') as storage_file:
            data = json.load(storage_file)
            prev_score = data['High score']
    except:
        prev_score = 0

    if replay_winner:
        replay_genome(config_path)
    else:
        run(config_path)