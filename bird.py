import pygame, sys, random, json
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
pygame.init()


#Sounds
flap_sound = pygame.mixer.Sound('Sounds/wing.wav')
death_sound = pygame.mixer.Sound('Sounds/hit.wav')
score_sound = pygame.mixer.Sound('Sounds/point.wav')

game_font = pygame.font.Font('04B_19.ttf',40)
settings_font = pygame.font.Font('04B_19.ttf',25)

def re_size(x):
    size = (int(x[0]*RELATIVE_PERCENT),int(x[1]*RELATIVE_PERCENT))
    return size


#Game csts
RELATIVE_PERCENT = 0.75 #This allows you to scale the whole game scale (100% = 576x1024)

BIRD_SIZE = (BIRD_WIDTH, BIRD_HEIGHT) = re_size((68,48))
PIPE_SIZE = (PIPE_WIDTH,PIPE_HEIGHT) = re_size((104,640))
BASE_SIZE = (BASE_WIDTH,BASE_HEIGHT) = re_size((672, 224))
BAR_SIZE = (BAR_WIDTH,BAR_HEIGHT) = re_size((120,15))
BAR_CHANGER_SIZE = (BAR_CHANGER_WIDTH,BAR_CHANGER_HEIGHT) = re_size((11,35))
MSG_SIZE = (MSG_WIDTH,MSG_HEIGHT) = re_size((368,534))
SETTINGS_SIZE = (SETTING_WIDTH,SETTING_WIDTH) = re_size((75,75))
BACKBUTTON_SIZE =  re_size((100,50))
GAME_SIZE = (WIDTH, HEIGHT) = re_size((576,1024))

NUMBERS_SIZE = re_size((48,72))
ICON_SIZE = re_size((32,32))
CHECKBOX_SIZE = re_size((30,30))
GAME_OVER_SIZE = re_size((384, 84))

FPS = 120
GRAVITY = 1/4
WHITE = (255,255,255)
GREY = (63,63,63)
LIGHT_GREY = (102,102,102)

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


def load_and_convert(path):
    img = pygame.image.load(path).convert_alpha()
    return img

def transform_scale(img,size):
    scaled_img = pygame.transform.scale(img,size)
    return scaled_img

#Un-ScaledImages
YELLOW_UPFLAP_IMG = load_and_convert('Images/yellowbird-upflap.png')
YELLOW_MIDFLAP_IMG =load_and_convert('Images/yellowbird-midflap.png')
YELLOW_DOWNFLAP_IMG = load_and_convert('Images/yellowbird-downflap.png')

BLUE_UPFLAP_IMG = load_and_convert('Images/bluebird-upflap.png')
BLUE_MIDFLAP_IMG = load_and_convert('Images/bluebird-midflap.png')
BLUE_DOWNFLAP_IMG = load_and_convert('Images/bluebird-downflap.png')

RED_MIDFLAP_IMG = load_and_convert('Images/redbird-upflap.png')
RED_UPFLAP_IMG = load_and_convert('Images/redbird-downflap.png')
RED_DOWNFLAP_IMG = load_and_convert('Images/redbird-midflap.png')

SETTINGS_IMG = load_and_convert('Images/settings.png')
ICON_IMG = load_and_convert('Images/favicon.ico')
MSG_IMG = load_and_convert('Images/message.png')
BASE_IMG = load_and_convert('Images/base.png')
UNCHECKEDBOX_IMG = load_and_convert('Images/uncheckedbox.png')
CHECKEDBOX_IMG = load_and_convert('Images/checkedbox.png')
BACKBUTTON_IMG = load_and_convert('Images/backbutton.png')
GAME_OVER_IMG = load_and_convert('Images/gameover.png')

GREEN_PIPE_IMG = load_and_convert('Images/pipe-green.png')
RED_PIPE_IMG = load_and_convert('Images/pipe-red.png')

DAY_BG_IMG = load_and_convert('Images/background-day.png')
NIGHT_BG_IMG = load_and_convert('Images/background-night.png')

#Scaled Images
YELLOW_DOWNFLAP = transform_scale(YELLOW_DOWNFLAP_IMG,BIRD_SIZE)
YELLOW_MIDFLAP = transform_scale(YELLOW_MIDFLAP_IMG,BIRD_SIZE)
YELLOW_UPFLAP = transform_scale(YELLOW_UPFLAP_IMG,BIRD_SIZE)

BLUE_DOWNFLAP = transform_scale(BLUE_DOWNFLAP_IMG,BIRD_SIZE)
BLUE_MIDFLAP = transform_scale(BLUE_MIDFLAP_IMG,BIRD_SIZE)
BLUE_UPFLAP = transform_scale(BLUE_UPFLAP_IMG,BIRD_SIZE)

RED_UPFLAP = transform_scale(RED_UPFLAP_IMG,BIRD_SIZE)
RED_MIDFLAP = transform_scale(RED_MIDFLAP_IMG,BIRD_SIZE)
RED_DOWNFLAP = transform_scale(RED_DOWNFLAP_IMG,BIRD_SIZE)

DAY_BG = transform_scale(DAY_BG_IMG,GAME_SIZE)
NIGHT_BG = transform_scale(NIGHT_BG_IMG,GAME_SIZE)

GREEN_PIPE = transform_scale(GREEN_PIPE_IMG,PIPE_SIZE)
RED_PIPE = transform_scale(RED_PIPE_IMG,PIPE_SIZE)

SETTINGS = transform_scale(SETTINGS_IMG,SETTINGS_SIZE)
ICON = transform_scale(ICON_IMG,ICON_SIZE)
MSG = transform_scale(MSG_IMG,MSG_SIZE)
BASE = transform_scale(BASE_IMG,BASE_SIZE)
UNCHECKEDBOX = transform_scale(UNCHECKEDBOX_IMG,CHECKBOX_SIZE)
CHECKEDBOX = transform_scale(CHECKEDBOX_IMG,CHECKBOX_SIZE)
CHECKBOXES = [UNCHECKEDBOX,CHECKEDBOX]
GAME_OVER = transform_scale(GAME_OVER_IMG,GAME_OVER_SIZE)
BACKBUTTON = transform_scale(BACKBUTTON_IMG,BACKBUTTON_SIZE)


YELLOW_BIRDFRAMES = [YELLOW_DOWNFLAP,YELLOW_MIDFLAP,YELLOW_UPFLAP]
BLUE_BIRDFRAMES = [BLUE_DOWNFLAP,BLUE_MIDFLAP,BLUE_UPFLAP]
RED_BIRDFRAMES = [RED_DOWNFLAP,RED_MIDFLAP,RED_UPFLAP]


pygame.display.set_icon(ICON)
pygame.display.set_caption('Flappy Bird') 

#Game Variables
data = {

    'High score': 0,
    'Check number':0,
    'Volume':.5

}

velocity = 0
baseX = 0
bird_index = 1
gameState = 'Restart'
can_score = True

try:
    with open('storage.txt') as storage_file:
        data = json.load(storage_file)
except:
    print("Storage not created yet!")

flap_sound.set_volume(data['Volume'])
death_sound.set_volume(data['Volume'])
score_sound.set_volume(data['Volume'])

high_score = data['High score']
score = 0

#Loop number
checkNum = data['Check number']

FRAMES = YELLOW_BIRDFRAMES
PIPE = GREEN_PIPE


bird_surface = FRAMES[bird_index]
mode_surface = settings_font.render('Night-Mode:',True,WHITE)
vol_surface = settings_font.render('Master-Volume:',True,WHITE)


vol_bar_surf = pygame.Surface([BAR_WIDTH,BAR_HEIGHT])
bar_changer_surf = pygame.Surface([BAR_CHANGER_WIDTH,BAR_CHANGER_HEIGHT])

vol_bar_surf.fill(LIGHT_GREY)
bar_changer_surf.fill(GREY)

bird_rect = bird_surface.get_rect(center = (100*RELATIVE_PERCENT,HEIGHT//2))
pipe_rect = PIPE.get_rect(center = (100*RELATIVE_PERCENT,HEIGHT//2))
game_over_rect = GAME_OVER.get_rect(center = (WIDTH//2,HEIGHT//2))
msg_rect = MSG.get_rect(center = (WIDTH//2,HEIGHT//2))
settings_rect = SETTINGS.get_rect(center = (WIDTH//2,300))
mode_rect = mode_surface.get_rect(center =(150*RELATIVE_PERCENT,120*RELATIVE_PERCENT))


checkbox_rect = CHECKBOXES[checkNum].get_rect(topleft = (mode_rect.x+mode_rect.width,mode_rect.y))
backbutton_rect = BACKBUTTON.get_rect(center = (150*RELATIVE_PERCENT-1.75*CHECKBOX_SIZE[0],50*RELATIVE_PERCENT))


vol_rect = vol_surface.get_rect(topleft = (mode_rect.x,mode_rect.y+mode_rect.height))
vol_bar_rect = vol_bar_surf.get_rect(midleft = (vol_rect.right,vol_rect.centery))
bar_changer_rect = bar_changer_surf.get_rect(center = (vol_bar_rect.centerx,vol_bar_rect.centery+1))

try:
    bar_changer_rect.centerx = data['Volume']*vol_bar_rect.width+vol_bar_rect.x
except:
    print("Storage not created yet!")

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
BIRDFLAP = pygame.USEREVENT + 1
MOUSE_EVENT = pygame.USEREVENT + 2


spawn_pipes_timer = pygame.time.set_timer(SPAWNPIPE,int(1200*RELATIVE_PERCENT))
flap_bird_timer = pygame.time.set_timer(BIRDFLAP,int(200*RELATIVE_PERCENT))

pipe_values = [400,600,800]
pipe_height = [value*RELATIVE_PERCENT for value in pipe_values]




def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            SCREEN.blit(PIPE,pipe)
        else:
            flipped_pipe = pygame.transform.flip(PIPE,False,True)
            SCREEN.blit(flipped_pipe,pipe)


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = PIPE.get_rect(midtop = (700*RELATIVE_PERCENT,random_pipe_pos))
    top_pipe = PIPE.get_rect(midbottom = (700*RELATIVE_PERCENT,random_pipe_pos - 300*RELATIVE_PERCENT))
    
    return bottom_pipe,top_pipe


def move_pipes(pipes):
    
    for pipe in pipes:
        pipe.centerx -= 5*RELATIVE_PERCENT

    visible_pipes = [pipe for pipe in pipes if pipe.right> 0]

    return visible_pipes 


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-velocity * 3,1)
    return new_bird


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return 'GameOver'
    if bird_rect.top <= -100*RELATIVE_PERCENT or bird_rect.bottom >= 900*RELATIVE_PERCENT:
        death_sound.play()
        can_score = True
        return 'GameOver'
    return 'Play'

def pipe_score_check():
    global score, can_score
    for pipe in pipe_list:
        if bird_rect.centerx-5<pipe.centerx<bird_rect.centerx+5 and can_score:
            score+=1
            can_score = False
            score_sound.play()
        if pipe.centerx < 0:
            can_score = True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,WHITE)
        score_rect = score_surface.get_rect(center = (WIDTH//2,100*RELATIVE_PERCENT))
        SCREEN.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}' ,True,WHITE)
        score_rect = score_surface.get_rect(center =(WIDTH//2,100*RELATIVE_PERCENT))
        SCREEN.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,WHITE)
        high_score_rect = high_score_surface.get_rect(center = (WIDTH//2,850*RELATIVE_PERCENT))
        SCREEN.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score>high_score:
        high_score = score
    return high_score

def bird_animation():
    new_bird = FRAMES[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            data['High score'] = high_score
            with open('storage.txt','w') as storage_file:
                json.dump(data,storage_file)
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            if gameState == "Settings":
                pygame.time.set_timer(MOUSE_EVENT,0)

        if event.type == MOUSEBUTTONDOWN:
            
            if gameState == "Restart":
                if msg_rect.collidepoint(event.pos):
                    score = 0
                    velocity = 0
                    gameState = "Play"
                    bird_rect.center = (100*RELATIVE_PERCENT,HEIGHT//2)
                    pipe_list.clear()
        
                if settings_rect.collidepoint(event.pos):
                    gameState = "Settings"
                
            if gameState == "Play":
                flap_sound.play()
                velocity = 0
                velocity -= 11*RELATIVE_PERCENT

            if gameState == "GameOver":
                gameState = "Restart"

            if gameState == "Settings":
                if checkbox_rect.collidepoint(event.pos):
                    if not checkNum:
                        checkNum = 1
                    else:
                        checkNum = 0
                        
                if backbutton_rect.collidepoint(event.pos):
                    gameState = 'Restart'
                if bar_changer_rect.collidepoint(event.pos) or vol_bar_rect.collidepoint(event.pos):
                    pygame.time.set_timer(MOUSE_EVENT,10)
                    
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (gameState == 'Play' or gameState == 'Pause'):
                if gameState == "Pause":
                    pipe_list.clear()
                    gameState = "Play"
                else:
                    gameState = "Pause"

            if event.key == pygame.K_SPACE:
                if gameState == "Play":
                    flap_sound.play()
                    velocity = 0
                    velocity -= 11*RELATIVE_PERCENT
                elif gameState == "Restart":
                    score = 0
                    velocity = 0
                    gameState = 'Play'
                    bird_rect.center = (100*RELATIVE_PERCENT,HEIGHT//2)
                    pipe_list.clear()
                elif gameState == "GameOver":
                    gameState = 'Restart'
                

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index+=1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()
        if event.type == MOUSE_EVENT and vol_bar_rect.left<pygame.mouse.get_pos()[0]<vol_bar_rect.right:
            bar_changer_rect.centerx = pygame.mouse.get_pos()[0]
            


    if checkNum:
        BG = NIGHT_BG
        PIPE = RED_PIPE
        FRAMES = RED_BIRDFRAMES
    else:
        BG = DAY_BG
        PIPE = GREEN_PIPE
        FRAMES = YELLOW_BIRDFRAMES

    SCREEN.blit(BG,(0,0))
    
    
    
    if gameState == "Play":
       

        rotated_bird = rotate_bird(bird_surface)
        SCREEN.blit(rotated_bird,bird_rect)
        draw_pipes(pipe_list)
        baseX -= 5*RELATIVE_PERCENT
        SCREEN.blit(BASE,(baseX,900*RELATIVE_PERCENT))
        SCREEN.blit(BASE,(baseX+BASE_WIDTH,900*RELATIVE_PERCENT))
        if baseX<-BASE_WIDTH:
            baseX = 0
        pipe_list = move_pipes(pipe_list)
        gameState = check_collision(pipe_list)
        velocity += GRAVITY
        bird_rect.centery += velocity
        pipe_score_check()
        score_display('main_game')

    elif gameState == "Pause":
        draw_pipes(pipe_list)
        SCREEN.blit(rotated_bird,bird_rect)
        
    elif gameState == "GameOver":
        draw_pipes(pipe_list)
        SCREEN.blit(rotated_bird,bird_rect)
        SCREEN.blit(GAME_OVER,game_over_rect)

    elif gameState == 'Settings':
        SCREEN.blit(BACKBUTTON,backbutton_rect)
        SCREEN.blit(mode_surface,mode_rect)
        SCREEN.blit(CHECKBOXES[checkNum],checkbox_rect)
        SCREEN.blit(vol_bar_surf,vol_bar_rect)
        SCREEN.blit(bar_changer_surf,bar_changer_rect)
        SCREEN.blit(vol_surface,vol_rect)
        flap_sound.set_volume((bar_changer_rect.centerx-vol_bar_rect.x)/(vol_bar_rect.width))
        death_sound.set_volume((bar_changer_rect.centerx-vol_bar_rect.x)/(vol_bar_rect.width))
        score_sound.set_volume((bar_changer_rect.centerx-vol_bar_rect.x)/(vol_bar_rect.width))

        data = {
            'High score': high_score,
            'Check number': checkNum,
            'Volume':(bar_changer_rect.centerx-vol_bar_rect.x)/(vol_bar_rect.width)
        }

    elif gameState == "Restart":
        SCREEN.blit(MSG,msg_rect)
        SCREEN.blit(SETTINGS,settings_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    SCREEN.blit(BASE,(baseX,900*RELATIVE_PERCENT))
    SCREEN.blit(BASE,(baseX+BASE_WIDTH,900*RELATIVE_PERCENT))
        

    pygame.display.update()
    clock.tick(FPS)





