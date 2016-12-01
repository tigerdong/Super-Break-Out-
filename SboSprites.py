'''
Author: Tiger Dong

Date: 04/15/2015

Description: Module containing sprites for the "Super Break-Out!" game.
'''

import pygame, random
pygame.init()

class Ball(pygame.sprite.Sprite):
    '''A class that defines the ball sprite for the game.'''
    
    def __init__(self, screen):
        '''Initializer method that creates a ball sprite.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)  
        
        #Sets the image and rect attributes
        self.__rest_height = 427
        self.image = pygame.Surface((10, 10))
        self.image.convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.last_rect_top = self.rect.top
        self.last_rect_bottom = self.rect.bottom
        self.last_rect_left = self.rect.left
        self.last_rect_right = self.rect.right
        self.rect.center = (screen.get_width()/2, self.__rest_height)
        self.__mouse = pygame.mouse.get_pos()
        
        #Attributes that track the screen surface and ball movement
        self.__paddle_length = 50
        self.__screen = screen
        self.__speed = 6
        if random.randint(0, 1) == 1:
            self.__dx = self.__speed
        else:
            self.__dx = -self.__speed
        self.__dy = self.__speed
        self.__atRest = True
        
    def change_direction_x(self):
        '''Method that reverts the x direction of the ball.'''
        self.__dx = -self.__dx
        
    def change_direction_y(self):
        '''Method that reverts the y direction of the ball.'''
        self.__dy = -self.__dy
    
    def get_last_rect_left(self):
        '''Accessor method that returns the previous left rect attribute of 
        the ball.'''
        return self.last_rect_left
    
    def get_last_rect_right(self):
        '''Accessor method that returns the previous right rect attribute of 
        the ball.'''
        return self.last_rect_right
    
    def get_last_rect_top(self):
        '''Accessor method that returns the previous top rect attribute of 
        the ball.'''
        return self.last_rect_top
    
    def get_last_rect_bottom(self):
        '''Accessor method that returns the previous bottom rect attribute of 
        the ball.'''
        return self.last_rect_bottom
        
    def reset_values(self):
        '''Method that resets the values of the ball.'''
        self.rect.center = (self.__mouse[0], self.__rest_height)
        if random.randint(0, 1) == 1:
            self.__dx = self.__speed
        else:
            self.__dx = -self.__speed
        self.__dy = self.__speed
        self.__atRest = True
        
    def in_motion(self):
        '''Method that sets the ball into motion.'''
        self.__atRest = False
        
    def shrink_paddle(self):
        '''Method that lets the ball know the paddle has shrunk.'''
        #Variable that makes sure the ball follows the paddle when at rest is
        #changed
        self.__paddle_length = 25
        
    def update(self):
        '''Method that updates the sprite.'''
        self.__mouse = pygame.mouse.get_pos()
        if self.__atRest == True:
            #If the ball is at rest, then it is to always be centered with the
            #paddle
            self.rect.center = (self.__mouse[0], self.__rest_height)
            if self.rect.right > (self.__screen.get_width() - \
                                  (50 + self.__paddle_length - 5)):
                self.rect.right = (self.__screen.get_width() - \
                                   (50 + self.__paddle_length - 5))
            elif self.rect.left < (50 + self.__paddle_length - 5):
                self.rect.left = (50 + self.__paddle_length - 5)
        else:
            #Values that keep track of where the ball was last
            #(Used for hit detection)
            self.last_rect_top = self.rect.top
            self.last_rect_bottom = self.rect.bottom
            self.last_rect_left = self.rect.left
            self.last_rect_right = self.rect.right
            #Ball movement
            self.rect.left += self.__dx
            self.rect.top -= self.__dy
            
                
class Paddle(pygame.sprite.Sprite):
    '''Class the defines the paddle sprite for the game.'''
    
    def __init__(self, screen):
        '''Initializer method that is run when the sprite is created.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)  
        
        #Sets the image and rect attributes
        self.image = pygame.Surface((100, 10))
        self.image.convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.__screen = screen
        self.rect.center = (self.__screen.get_width()/2, 440)
        self.__shrink_down = 0
        
    def shrink_paddle(self):
        self.__shrink_down = 50
    
    def update(self):     
        '''Method that updates the sprite.'''
        self.__mouse = pygame.mouse.get_pos()
        if self.__shrink_down > 0:
            self.image = pygame.Surface(((50 + self.__shrink_down), 10))
            self.image.convert()
            self.__color = 255 - ((self.__shrink_down % 10) * 15)
            self.image.fill((self.__color, self.__color, self.__color))
            self.rect = self.image.get_rect()
            self.__shrink_down -= 1
        self.rect.center = (self.__mouse[0], 440)
        if self.rect.left < 50:
            self.rect.left = 50
        elif self.rect.right > (self.__screen.get_width() - 50):
            self.rect.right = (self.__screen.get_width() - 50)
            
class SideWall(pygame.sprite.Sprite):
    '''Class that defines the side walls for the game.'''
    
    def __init__(self, screen, x):
        '''Initializer method that is run when the sprite is created.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)  
        
        #Sets the image and rect attributes
        self.image = pygame.Surface((50, 430))
        self.image.convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.__screen = screen
        self.rect.left = x
        self.rect.bottom = self.__screen.get_height()   
        
class TopWall(pygame.sprite.Sprite):
    '''Class that defines the top wall for the game.'''
    
    def __init__(self):
        '''Initializer method that is run when the sprite is created.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)  
        
        #Sets the image and rect attributes
        self.image = pygame.Surface((640, 50))
        self.image.convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 50
        
class Brick(pygame.sprite.Sprite):
    '''Class that defines the brick for the game.'''
    
    def __init__(self, color, x, y):
        '''Initializre method that is run when the sprite is created.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Sets the image and rect attributes
        self.image = pygame.Surface((30, 13))
        self.image.convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''Class that defines a label sprite to display the score.'''
    
    def __init__(self):
        '''Initializer loads the custom font "8-Bit Wonder", sets score to 0,
        and lives to 3.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        #Loads custom font, and initializes the starting score and life total
        self.__font = pygame.font.Font("PressStart2P.ttf", 25)
        self.__score = 0
        self.__lives = 3
         
    def scored(self, score):
        '''method that adds the value 'score' to the score.'''
        self.__score += score
        
    def remove_life(self):
        '''Method that subtracts one from the player's lives.'''
        self.__lives -= 1
        
    def get_lives(self):
        '''Accessor method that returns the number of lives.'''
        return self.__lives
    
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Lives:%d Point(s):%d" %\
                (self.__lives, self.__score)
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 22)

class Label(pygame.sprite.Sprite):
    '''Class that defines a label sprite to display the end game message.'''
    
    def __init__(self, message, font_size, x, y):
        '''Initializer loads the custom font "8-Bit Wonder"'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        #Loads custom font, and sets the message and coordinates
        self.__font = pygame.font.Font("PressStart2P.ttf", font_size)
        self.__message = message
        self.__x = x
        self.__y = y
        
    def set_message(self, message):
        '''Mutator method that sets the message.'''
        self.__message = message
        
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.__x, self.__y)
    
class Boundary(pygame.sprite.Sprite):
    '''Class that defines a boundary at the bottom of the screen.'''
    
    def __init__(self, screen):
        '''Initializer method that gets called when the sprite is created.'''
        #Calls the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Sets sprite rect attributes
        self.__screen = screen
        self.image = pygame.Surface((self.__screen.get_width(), 1))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = (self.__screen.get_height())