from pathlib import Path

import pygame, sys, random

def draw_floor(): #will allow us to update floor as it moves along
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #picks a random number from pipe height
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos)) #Spawns pipes on the farther side of the screen at 700, at randomly-chosen heights from our pipe height list. This is the
    #bottom pipe, with randomly-generated height, while the following top_pipe is spawned just above it
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    #pass in the list of all pipe rectangles
    for pipe in pipes:
        pipe.centerx -= 5 #takes all pipe rectangles, moves them to the left by a little bit
    return pipes #returns a new list of pipes

def draw_pipes(pipes):
    #cycle through all pipes in the list and draw on screen
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        #check if any of these pipes are colliding with our bird
        if bird_rect.colliderect(pipe):
            #play death sound when we hit a pipe
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index] #updates the bird
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state): #will take in a parameter that allows the function
    #to display the current score when game is active, and when game is over,
    #it will display high score AND current score
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score): #want to update the high score
    if score > high_score:
        high_score = score
    return high_score

#test for pathlib
path_for_text = Path("Users/Owner/Desktop/Coding/PyGame - FlappyBird/FlappyBird_Python-master/FlappyBird_Python-master")

#pre-init initiates the mixer in a specific way, ahead of time
pygame.mixer.pre_init(frequency = 48000, size = -16, channels = 1, buffer = 2048)
pygame.init()
screen = pygame.display.set_mode((576, 1024))  # store a display within a variable; width,
# height dimensions of screen. Work well with file sizes
clock = pygame.time.Clock() #allows us to keep track of frame rate
font_file = path_for_text / "04B_19.TTF"
game_font = pygame.font.Font("C:/Users/Owner/Desktop/Coding/PyGame - FlappyBird/FlappyBird_Python-master/FlappyBird_Python-master/04B_19.TTF",40) #this isn't loading properly!

#Game Variables
#need to create gravity so the bird falls
gravity = 0.25
bird_movement = 0 #will apply to bird
game_active = True #determines whether the game is active, or not


score = 0
high_score = 0

bg_surface = pygame.image.load('C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface) #scales up our background image onto the display surface

floor_surface = pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)

floor_x_pos = 0 #determines position of floor while moving

bird_downflap = pygame.transform.scale2x(pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0 #used to pick a surface from the list
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

#let's import picture of bird
#bird_surface = pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\bluebird-midflap.png").convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,512)) #takes our new bird surface nad puts a rectangle around it

#Adding pipes
pipe_surface = pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\flappy-bird-assets-master\\flappy-bird-assets-master\\sprites\\pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] #list that will house pipes being added
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400, 600, 800] #list of possible heights for all pipes to have; every time we create a new pipe we pick a number from this list randomly

game_over_surface = pygame.transform.scale2x(pygame.image.load("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\FlappyBird_Python-master\\FlappyBird_Python-master\\assets\\message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

#want our bird to make a flap sound everytime we hit the space bar
flap_sound = pygame.mixer.Sound("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\FlappyBird_Python-master\\FlappyBird_Python-master\\sound\\sfx_wing.wav")
death_sound = pygame.mixer.Sound("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\FlappyBird_Python-master\\FlappyBird_Python-master\\sound\\sfx_hit.wav")
score_sound = pygame.mixer.Sound("C:\\Users\\Owner\\Desktop\\Coding\\PyGame - FlappyBird\\FlappyBird_Python-master\\FlappyBird_Python-master\\sound\\sfx_point.wav")
score_sound_countdown = 100


while True:
    # for example, image of player 1, and a background image
    for event in pygame.event.get():  # looks for all currently-occuring
        # events in the game
        if event.type == pygame.QUIT:  # input done by clicking the
            # exit button in the game window
            pygame.quit()  # actually quits for you
            sys.exit()
        if event.type == pygame.KEYDOWN: #checks for player input, with any key being pressed down
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 #disables all gravity effects, and just applies speed of jump below
                bird_movement -= 12
                flap_sound.play() #plays the flap sound
            if event.key == pygame.K_SPACE and game_active == False:
                #only runs if we press space and if game is over
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0 #resets the score to zero at the start of a new game

        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe()) #extends the pipe list with the tuple elements, bottom and top pipes


        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation() #puts a new rectangle around each new image for the animation
    screen.blit(bg_surface,(0,0))

#The bird and the pipes should only be on the screen when the game is active

    if game_active:

        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        # let's apply the bird_movement to our bird rectangle
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)  # runs the move pipes function on our previous pipes list, and replaces the old pipe list with the updated pipe list
        draw_pipes(pipe_list)

        #want to update the score
        score+=0.01 #increases the score as time goes on.
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else: #if game is over, we wanna display high score
        #want to update high score before we display
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576: #when floor_x_pos gets to -576 (when the base "block" has moved far enough to the left), we reset floor_x_pos to 0, thus restarting base position and loop
        floor_x_pos = 0

    #screen.blit(floor_surface, (floor_x_pos,900))

    pygame.display.update()  # anything drawn in while loop before this code, draws it on the screen
    clock.tick(120) #when game runs, it can run at a maximum of 120 frames per sec; it CAN run slower, though