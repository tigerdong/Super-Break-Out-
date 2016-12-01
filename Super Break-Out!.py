'''
Author: Tiger Dong

Date: 04/15/2015

Description: Single player game where the objective is to clear all of the
bricks on the screen by bouncing a ball off of the bricks.
'''

#Import and Initialize
import pygame, SboSprites
pygame.init()
screen = pygame.display.set_mode((640, 480))

def check_collision(ball, bricks):
    '''Function that checks which side of the bricks the ball collided with.'''
    
    #Boolean variables that keep track of whether there is a collision on the
    #top/bottom or left/right
    x_collide = False
    y_collide = False
    
    #A for loop that checks if the collision is on the top/bottom or left/right
    for brick in range(len(bricks)):
        if ((ball.rect.top <= bricks[brick].rect.bottom and \
             ball.get_last_rect_top() >= bricks[brick].rect.bottom) or \
            (ball.rect.bottom >= bricks[brick].rect.top and \
             ball.get_last_rect_bottom() <= bricks[brick].rect.top)) and \
           (ball.rect.right >= bricks[brick].rect.left and \
            ball.rect.left <= bricks[brick].rect.right):
            y_collide = True
        if ((ball.rect.left <= bricks[brick].rect.right and \
             ball.get_last_rect_left() >= bricks[brick].rect.right) or \
            (ball.rect.right >= bricks[brick].rect.left and \
             ball.get_last_rect_right() <= bricks[brick].rect.left)) and \
           (ball.rect.bottom >= bricks[brick].rect.top and \
            ball.rect.top <= bricks[brick].rect.bottom):
            x_collide = True
            
    if y_collide == True:
        return 1
    elif x_collide == True:
        return 2
    else:
        return 0
    
def main():
    '''Main function that outlines the program.'''
    
    #Display Configuration
    pygame.display.set_caption("Super Break-Out!")
    
    #Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    #Sounds
    pygame.mixer.music.load("background_music.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    boing = pygame.mixer.Sound("boing.wav")
    boing.set_volume(0.8)   
    death = pygame.mixer.Sound("death.wav")
    death.set_volume(1.0) 
    break_brick = pygame.mixer.Sound("break_brick.wav")
    break_brick.set_volume(1.0) 
    shrink = pygame.mixer.Sound("shrink.wav")
    shrink.set_volume(1.0) 
    
    #Sprites
    ball = SboSprites.Ball(screen)
    paddle = SboSprites.Paddle(screen)
    boundary = SboSprites.Boundary(screen)
    
    leftWall = SboSprites.SideWall(screen, 0)
    rightWall = SboSprites.SideWall(screen, 590)
    topWall = SboSprites.TopWall()
    sideWalls = pygame.sprite.Group(leftWall, rightWall)
    
    #A for loop that uses a colors list to create a list and group of bricks
    colors = [(255, 0, 255), (255, 0, 0), (255, 255, 0), (255, 128, 0), \
              (0, 255, 0), (0, 0, 255)]
    brickList = [[], [], [], [], [], []]
    brickGroup = []
    brick_x = 50
    brick_y = 160
    for row in range(6):
        brick_x = 50
        for col in range(18):
            brick = SboSprites.Brick(colors[row], brick_x, brick_y)
            brickList[row].append(brick)
            brick_x += 30
        brickGroup.append(pygame.sprite.Group(brickList[row]))
        brick_y += 13
    #Group of every row of bricks is created
    allBricks = pygame.sprite.Group(brickGroup[0], brickGroup[1], \
                                    brickGroup[2], brickGroup[3], \
                                    brickGroup[4], brickGroup[5])
    
    scorekeeper = SboSprites.ScoreKeeper()
    #The end game labels aren't given a message until a boolean 'game_over' 
    #is True
    end_message_label = SboSprites.Label("", 50, 320, 240)
    any_key_label = SboSprites.Label("", 20, 320, 280)
    
    allSprites = pygame.sprite.OrderedUpdates(ball, paddle, sideWalls, topWall,\
                                              allBricks, scorekeeper, \
                                              end_message_label, any_key_label)
    
    #ACTION
    
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    #Number of bricks left
    total_bricks = 108
    #Boolean values to keep track of game state
    game_over = False
    shrunk = False
    #Hides the mouse
    pygame.mouse.set_visible(False)
    
    #Loop    
    while keepGoing:
        
        #Time
        clock.tick(30)
        
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                ball.in_motion()
                
        #Multiple-Sprite Collision Detection and Reporting   
        if (ball.rect.bottom >= paddle.rect.top) and \
           (ball.rect.top < (paddle.rect.top - 6)) and \
           (ball.rect.left < paddle.rect.right) and \
           (ball.rect.right > paddle.rect.left):
            ball.change_direction_y()
            boing.play()
        if ball.rect.colliderect(topWall.rect):
            ball.change_direction_y()
            boing.play()
        if ball.rect.colliderect(boundary.rect):
            ball.reset_values()
            scorekeeper.remove_life()
            death.play()
        if pygame.sprite.spritecollide(ball, sideWalls, False):
            ball.change_direction_x()
            boing.play()
        for index in range(len(brickGroup)):
            bricks_collided = pygame.sprite.spritecollide(ball, \
                                                          brickGroup[index], \
                                                          True)
            if bricks_collided:
                if check_collision(ball, bricks_collided) == 1:
                    ball.change_direction_y()
                elif check_collision(ball, bricks_collided) == 2:
                    ball.change_direction_x()
                break_brick.play()
            for scored in range(len(bricks_collided)):
                #Code that is run when a brick is destroyed
                scorekeeper.scored(6 - index)
                total_bricks -= 1
                for row in range(len(brickList)):
                    for col in range(len(brickList[row])):
                        brickList[row][col].rect.top += 1
        
        #When half of the bricks are gone, the paddle shrinks
        if (total_bricks <= 54) and (shrunk == False):
            #A boolean 'shrunk' is set to True so that the event is not repeated
            shrunk = True
            ball.shrink_paddle()
            paddle.shrink_paddle()
            shrink.play()
        #When there are no bricks or lives left, the game ends
        if total_bricks == 0:
            game_over = True
            end_message_label.set_message("You Win!")
            any_key_label.set_message("Press any key to exit")
        if scorekeeper.get_lives() == 0:
            game_over = True
            end_message_label.set_message("Game Over!")
            any_key_label.set_message("Press any key to exit")
        
        #Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
            
        pygame.display.flip()      

        #A while loop waits for the player to press any key before closing the
        #window
        if game_over == True:
            pygame.mixer.music.set_volume(0)
            while keepGoing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or \
                       event.type == pygame.KEYDOWN:
                        keepGoing = False  
    #Unhides the mouse
    pygame.mouse.set_visible(True)
    
    #Closes main window
    pygame.quit()
    
#Calls main function
main()