import pygame
import random
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): #inherit from another class ##sprite is a rectangle combined
    def __init__(self):
        super().__init__() #initialising sprite class inside the initialisation of the Player class
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2] #selfed this is one to make it available to all the methods inside the class
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25)

    def player_input(self):
       keys =  pygame.key.get_just_pressed()
       if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
           self.gravity = -20
           self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 150
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill() #destroy the class Obstacle that went outside the frame


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obstacle_rec in obstacle_list:
#             obstacle_rec.x -= 5

#             if obstacle_rec.bottom == 300:
#                 screen.blit(snail_surface, obstacle_rec)
#             else:
#                 screen.blit(fly_surface, obstacle_rec)

#         #delete rectangles if they leave too much out of the screen
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

#         return obstacle_list
#     else :
#         return []
    

# def collisions(player, obstacles):
#     if obstacles:
#         for obstacles_rect in obstacles:
#             if player.colliderect(obstacles_rect):
#                 return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False): #sprite, group, bool, #False means snail will not be deleted
        obstacle_group.empty()
        return False
    else:
        return True

# def player_animation():
    global player_surface, player_index #whatever change in value is happeing here will also be reflected to the main and won't just stay localised inside this function
    
    #player walking animation if player is on floor
    if player_rect.bottom < 300:
        player_surface = player_jump
        
    #display the jump surface if the player is not on the floor
    else:
        player_index += 0.1 #to slow down the walking process
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

    
    

##starting variables
pygame.init() ##to run any pygame code, starts pygame to develop a game. Example starting the engine of a car
##display surface
screen = pygame.display.set_mode((800, 400)) ##set_mode((width, height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() #Clock object
font = pygame.font.Font('font/Pixeltype.ttf', 50) #font type , font size
game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)


#============================== Obstacle Start ==============================
player = pygame.sprite.GroupSingle() #contains all the sprite that we can access
player.add(Player())

obstacle_group = pygame.sprite.Group()
#============================== Obstacle Start ==============================


##test_surface = pygame.Surface((100,200))
##test_surface.fill('Red')

sky_surface = pygame.image.load('graphics/Sky.png').convert() #any graphical import is a new surface
ground_surface = pygame.image.load('graphics/ground.png').convert()
#text_surface = test_font.render('My game', False, 'Black') #test, antialiase = smooth edge, colour

#score_surface = font.render('My Game', False, 'Black')
#score_rect = score_surface.get_rect(center = (400, 50))



#Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #.convert_alpha() for faster display on the screen while preserving any per-pixel transparency
#snail_x_pos = 600
# snail_rect = snail_surface.get_rect(bottomright = (600, 300))

fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []


#player
# player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# player_surface = player_walk[player_index]
# player_rect = player_surface.get_rect(midbottom = (80, 300)) #pygame.Rect() #left, top, width, height : this is the basic func calling but since we can draw a rect around using the get function from the player we use this #### to detect basic collisions and for precise positions
# player_gravity = 0



#intro to screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
##player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) #(surface, rotation, scale)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 330))


#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) #(the event we want to trigger, how often we want to trigger in ms)

##loop to keep the code runing forever
while True: ##The True makes the loop run forever

    #very imp player input is to close the game
    #checking all the possible player input is called event loop
    for event in pygame.event.get(): # Event loop - runs once per frame
        if event.type == pygame.QUIT: ##Quit is the most common event types from the documentation
            pygame.quit() #pygame.error: video system not initialized is generated because it's the polar opposit of pygame.init(). AKA it will uninitialise. that will not cause the display update to run
            #best way to stop is to use system module instead of using break to break from the module
            #from sys import exit function
            exit() #make the while true loop disappear, to ensure the Python script itself stops running
        
        if game_active:
            # if event.type == pygame.MOUSEBUTTONDOWN: #this is true if we move the mouse
            #     if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: #collidepoint gives the tuple of x,y position that checks with the event.pos values ##event,pos is the mouse positon touching the player to cause the player to jump
            #         player_gravity = -20
            #         #print('downMouse')
            
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
            #         player_gravity = -20
            #         # print('down')

            if event.type == obstacle_timer:

                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

                # if randint(0, 2): #gives values of 0 to 1 where 0 is false and 1 is true
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100), 150)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
  
                start_time = int(pygame.time.get_ticks() / 1000)



    #draw all the elements
    #update everything
    if game_active:
        screen.blit(sky_surface, (0,0)) #(surface, pos(left, top)) screen.blit = draw a source Surface onto another Surface (the destination) at a specified position
        screen.blit(ground_surface, (0,300))

        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score_surface, score_rect)
        score = display_score()


        #============================== Obstacle Start ==============================
        #snail_x_pos -= 4
        #if snail_x_pos < -100: snail_x_pos = 800

        # snail_rect.x -= 4
        # if snail_rect.right <= 0 : snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        obstacle_group.draw(screen)
        obstacle_group.update()


        #============================== Obstscle End ==============================
        #============================== Player Start ==============================
        #player_rect.left += 1

        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rect)

        #Sprite functionality
        player.draw(screen) #draws sprites
        player.update() #updates sprites
        #============================== Player End ==============================
        #============================== Collision Start ==============================
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        #     print('Works')
        # game_active = collisions(player_rect, obstacle_rect_list)

        game_active = collision_sprite()
        #============================== Collision Start ==============================
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        obstacle_rect_list.clear()

        # player_rect.midbottom = (80, 300)
        # player_gravity = 0
        

        score_mssage = font.render(f'Your score: {score}', False, (111,196,169))
        score_mssage_rect = score_mssage.get_rect(center = (400, 330))

        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_mssage, score_mssage_rect)

    #if player_rect.collidedict(snail_rect)
    #mouse_pos = pygame.mouse.get_pos()
    #player_rect.collidepoint(mouse_pos)

    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:


    pygame.display.update() #this is to update the code written above to the screen
    clock.tick(60)#how fast the frame will run