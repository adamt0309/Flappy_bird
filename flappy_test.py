import pygame, sys, random

#testing commit 1


#Defining the fuctions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (300, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (300, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:

        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -10 or bird_rect.bottom >= 400:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 4.5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'Main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'Game over':
        score_surface = game_font.render(f'Score:  {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center = (100, 375))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#The line below was to make the sound quality better for some computers, but it didn't work for this one
#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

#The screen size
Screen_width = 288
Screen_height = 512

#The window/game settings(for a lack of a better comment)
pygame.init()
screen = pygame.display.set_mode((Screen_width, Screen_height))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)

#game variables
gravity = 0.1
bird_movement = 0
game_active = True
score = 0
high_score = 0

#Background
bg_surface = pygame.image.load("assets/background-day.png").convert()

#the floor and the position of the floor
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

#the bird frames and images
bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 144))

#making the bird flap it's wings
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

#loading the pipe and calling the functions
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
pipe_height = [200, 250, 300]

#loading the starting screen
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))

#loading the sounds of it
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

#Main game loop
while True:
    #being able to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            #flapping the bastard
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()

            #if the game is over this is the retry and restarting the game
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 144)
                bird_movement = 0
                score = 0

        #spawning the pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        #cycling throught the bird images
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0,0))

    #the gravity and the bird moving
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        game_active = check_collision(pipe_list)

        screen.blit(rotated_bird, bird_rect)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('Main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('Game over')

    #floor
    floor_x_pos -= 1 
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    screen.blit(floor_surface, (floor_x_pos, 400))

    pygame.display.update()
    clock.tick(120)