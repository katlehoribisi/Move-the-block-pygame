import pygame, random, os

#Initialize pygame and create clock
pygame.init()
pygame.font.init()


clock = pygame.time.Clock()

#Create screen
WIDTH = 1200
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Move The Block!")

#Colors
BLACK = (0,0,0)
GREY = (10,10,10)
WHITE = (255,255,255)
RED = (225,50,60)
DARK_RED = (90,20,60)

#Game settings
VELOCITY = 18
GRAVITY = 9.8
jump = False
jump_y = 20
movement = [False,False]
top = False
move_box_velocity = 8
move_floor = [5,-5]


score = 0 
timer = 3

#Obstacles
box = pygame.Rect(WIDTH//2-20,50,80,80)

floor_button = pygame.Rect(WIDTH-100,HEIGHT//2+340,80,80)

#Images
player = pygame.image.load("C:/Users/katle/OneDrive/Desktop/Code/my_py_game/assets/Pink_Monster/Pink_Monster.png").convert()

flipped = [False,True]

player = pygame.transform.scale(player,(86,86))
player_rect = player.get_rect()
player_rect.centerx = WIDTH//2
player_rect.y = HEIGHT//2

# TEXT
font = pygame.font.Font("C:/Users/katle/OneDrive/Desktop/Code/my_py_game/assets/Font/Planes_ValMore.ttf", 32)
font2 = pygame.font.Font("C:/Users/katle/OneDrive/Desktop/Code/my_py_game/assets/Font/Planes_ValMore.ttf", 64)
gameHeader = font.render("Move The Block!",True,DARK_RED)
gameHeader_rect = gameHeader.get_rect()
gameHeader_rect.centerx = WIDTH//2
gameHeader_rect.y = 50

gameover = font2.render("Game Over!",True,BLACK)
gameover_rect = gameover.get_rect()
gameover_rect.x = WIDTH//2-170
gameover_rect.y = HEIGHT//2-50

pressAnyKey = font.render("Press Any Key To Play Again.",True,GREY)
pressAnyKey_rect = pressAnyKey.get_rect()
pressAnyKey_rect.x = WIDTH//2-230
pressAnyKey_rect.y = HEIGHT//2+30

# Game sounds
box_out = pygame.mixer.Sound("Music/YOP.wav")
box_drop = pygame.mixer.Sound("Music/WUP.wav")
pygame.mixer.music.load("Music/jooz.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


# Game pause
def paused():
    pause = True
    
    while pause:
        screen.blit(gameover,gameover_rect)
        screen.blit(pressAnyKey,pressAnyKey_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                pause = False

#Game loop
looping = True
while looping:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movement[0] = True


                if flipped[1]:
                    flip = pygame.transform.flip(player,True,False)
                    player = flip
                    flipped[1] = False
                    flipped[0] = True

            if event.key == pygame.K_d:
                movement[1] = True

                if flipped[0]:
                    flip = pygame.transform.flip(player,True,False)
                    player = flip
                    flipped[0] = False
                    flipped[1] = True
                    
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movement[0] = False
            if event.key == pygame.K_d:
                movement[1] = False
        

    #Fill screen for updating from old
    screen.fill(WHITE)

    #Obstacles drawn
    pygame.draw.rect(screen,DARK_RED,box)
    pygame.draw.rect(screen,RED,floor_button)


    # Danger box collide
    if box.colliderect(floor_button):

        box_out.play()
        rand = random.randint(50,1100)
        box.x = rand
        box.y = 50
        timer -= 1

        # Reset game values
        if timer == 0:

            move_box_velocity = 8
            VELOCITY = 18
            move_floor[1] = -5

            paused()
            score = 0
            timer = 3
            rand = random.randint(50,1100)
            box.x = rand
            box.y = 50
            player_rect.x = WIDTH//2
            # player_rect.bottom = HEIGHT//2-5
            jump_y = 20
            jump = False

    #Collide with box
    collision_tolerance_left = 20
    collision_tolerance_right = 50

    if player_rect.colliderect(box):

        # print(player_rect.right - box.left)
        #Left
        if(player_rect.right  - box.left) < collision_tolerance_left:
            player_rect.right = box.left
            pygame.Rect.move_ip(box,move_box_velocity,0)

        #Right
        if (player_rect.right  - box.right) > collision_tolerance_right:
            player_rect.left = box.right
            pygame.Rect.move_ip(box,-move_box_velocity,0)
        #TOP
        if (player_rect.bottom  - box.top) < collision_tolerance_left:
            player_rect.bottom = box.top
        
    #Box gravity
    if (box.bottom < HEIGHT-6):
        box.y += GRAVITY
        
    # if box out of screen
    if (box.right < 0 or box.left > WIDTH):
        score += 1
        box_drop.play()

        # rand x integer
        rand_box = random.randint(60,1100)

        box.right = rand_box
        box.y = 0

        # Make block, character and floor move faster
        move_box_velocity += 1
        VELOCITY += 1

        # # Randomly disperse floor
        # rand_floor = random.randint(50,1100)
        # floor_button.x = rand_floor

    # Regularly move floor
    floor_button.x += move_floor[1]
    if floor_button.x < 0:
        floor_button.x = WIDTH + 10
        move_floor[1] += -0.5


    #Character movement
    if player_rect.bottom < HEIGHT-5:
        player_rect.y += GRAVITY

    #Catch keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        jump = True
        # print(True)

    #Move left
    if movement[0] and player_rect.x > 0:
        player_rect.x -= VELOCITY

    #Move right
    if movement[1] and player_rect.x < WIDTH-70:
        player_rect.x += VELOCITY
        player = player
        
    #Do jump code
    if jump:
        player_rect.y -= jump_y
        jump_y += 12
        if jump_y > 90:
            jump_y = 90
            player_rect.y += jump_y
            jump = False

    # If on floor reset
    if player_rect.bottom > HEIGHT-5:
        jump_y = 20
        # print(jump_y)

    # Draw things
    score_text = font.render("Score: "+ str(score),True, DARK_RED)
    score_rect = score_text.get_rect()
    score_rect.x = 30
    score_rect.y = 50

    # Timer for game
    timer_text = font.render("Chances Left : "+ str(timer),True, DARK_RED)
    timer_rect = timer_text.get_rect()
    timer_rect.x = WIDTH-290
    timer_rect.y = 50

    #Blit images
    screen.blit(player,player_rect)
    screen.blit(gameHeader,gameHeader_rect)
    screen.blit(score_text,score_rect)
    screen.blit(timer_text,timer_rect)

    #Update game and tick clock
    pygame.display.update()
    clock.tick(60)

pygame.quit()

