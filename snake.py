# IMPORT FUNCTION 
import pygame 
import random
import os 
import time

# FOR MUSIC 
pygame.mixer.init()

pygame.init()

# COLOURS
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
yellow = (255,255,0)
pink = (231, 84, 128)

# CREATING WINDOWS
screen_width = 1200
screen_height = 700 
gamewindow = pygame.display.set_mode((screen_width , screen_height))

# BACKGROUND IMAGE 
bgimg = pygame.image.load("i:\MUSIC AND PHOTOS\download.jfif")
bgimg = pygame.transform.scale(bgimg , (screen_width, screen_height)).convert_alpha()


# GAME TITLE
pygame.display.set_caption(" MY FIRST GAME")
pygame.display.update()
Clock = pygame.time.Clock()
font = pygame.font.SysFont(None , 55)


# OTHER GAME FUNCTION WITH GAME SPECIFIER 

# FUNCTION TO DISPLAY TEXT ON SCREEN
def text_screen (text , color , x ,y ):
    screen_text = font.render(text , True , color)
    gamewindow.blit(screen_text,[x,y])

# FUNCTION TO DRAW SNAKE (HEAD + BODY)
def plot_snake (gamewindow , color ,snk_list ,snake_size):
    for i ,(x,y) in enumerate (snk_list):
        if i == len (snk_list)-1:
            pygame.draw.rect(gamewindow, (255,255,0),[x,y,snake_size,snake_size])                               # head
        else:
            pygame.draw.rect(gamewindow, (217, 1, 102),[x,y,snake_size,snake_size])                               # body

def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.blit(bgimg, (0, 0))
        if int (time.time()*2)%2 == 0:
            text_screen("BACK TO CHILDHOOD 🐍LET'S PLAY AGAIN !", white , 260 , 250)
            text_screen("Press space bar to play " , white, 232 , 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('i:\\MUSIC AND PHOTOS\\background music.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
        
        pygame.display.update()
        Clock.tick(30)                        # game loop speed 

# CREATING A GAME LOOP 
def gameloop():
    exit_game = False
    game_over = False    
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # CHECK IF HIGHSCORE FILE EXISTS
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open ("highscore.txt", "r") as f :
        highscore = f.read()

    snake_size = 20 

    foods = []
    for i in range (3):
        x = random.randrange( 0 , screen_width , snake_size)
        y = random.randrange( 0 , screen_height ,snake_size)
        foods.append([x,y])
    
    score = 0 
   
    init_velocity = snake_size
    fps = 8
    
    while not exit_game:
        if game_over:
            with open ("highscore.txt" , "w") as f :
                f.write(str(highscore))
            gamewindow.fill(white)
            text_screen("Oops! Snake died 😢 Press enter to continue " ,(20 , 30 ,60), 250 , 250 )
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = init_velocity
                        velocity_y = 0 

                    if event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = - init_velocity
                        velocity_y = 0 

                    if event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y =  - init_velocity
                        velocity_x = 0 

                    if event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = init_velocity
                        velocity_x = 0 

                    if event.key == pygame.K_q:
                        score +=10
                        fps +=0.5 

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            
            for food in foods:
                if abs (snake_x - food[0]) < snake_size and abs (snake_y - food [1]) <snake_size:
                    pygame.mixer.music.load('i:\\MUSIC AND PHOTOS\\eating sound.mp3')
                    pygame.mixer.music.play()
                    score+=10
                    food_x = random.randint(0, screen_width//2)
                    food_y = random.randint(0 , screen_height//2)
                    snk_length += 1
                    food [0] = random.randrange(0, screen_width, snake_size)
                    food [1] = random.randrange(0, screen_height, snake_size)
                    if score>int(highscore):
                        highscore = score
            
            gamewindow.fill(white)
            gamewindow.blit(bgimg , (0,0))
            text_screen("Score: " + str(score) + "Highscore: " +str(highscore), white , 5 ,5 )
            for food in foods :
                pygame.draw.circle(gamewindow , red, (food[0]+ snake_size//2,food[1]+snake_size//2),snake_size//2)
    
            head = []
            head.append (snake_x)
            head.append (snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('i:\\MUSIC AND PHOTOS\\mario_game_over_sms.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('i:\\MUSIC AND PHOTOS\\mario_game_over_sms.mp3')
                pygame.mixer.music.play()
            plot_snake(gamewindow , black , snk_list , snake_size)
        pygame.display.update()
        Clock.tick(fps)
        
    return 
welcome()