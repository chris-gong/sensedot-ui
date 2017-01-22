'''
Created on Jul 7, 2016

@author: Chris Gong
'''

import pygame
import serial
import time
import random

import MazeDatabase
import Stack

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        """ Constructor function """
 
        #Call the parent's constructor
        super().__init__()
 
        #Make a colored wall, of the size specified in the parameters
        #two lines of code below are outdated as the new implementation utilizes image graphics instead
        '''
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        '''
        if(width >= 100):
            img = pygame.image.load("woodrow.png")
            img = pygame.transform.scale(img, (width, 10))
            self.image = img
        else:
            img = pygame.image.load("woodcolumn.png")
            img = pygame.transform.scale(img, (10, height))
            self.image = img
        
        #Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    def equals(self, wall2):
        if(self.rect.x == wall2.rect.x and self.rect.y == wall2.rect.y):
            return True
        else:
            return False
    
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        #u means up as in facing up
        self.orientation = 'u'
        self.image = image
        
        #makes a player of specified position coordinates and sprite image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.actualX = x
        self.actualY = y
        
    #method checks if there is a wall by the player's left side
    #depending on the direction of the player's sprite
    def nearLeft(self, walls):
        bool = False
        original_x = self.rect.x
        original_y = self.rect.y
        if(self.orientation == 'u'):
            self.rect.x -= 50;
        elif(self.orientation == 'l'):
            self.rect.y += 50;
        elif(self.orientation == 'd'):
            self.rect.x += 50;
        else:
            self.rect.y -= 50;
            
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            bool = True
        #reset player's position back to normal
        self.rect.x = original_x
        self.rect.y = original_y
        return bool
    
    #method checks if there is a wall by the player's right side  
    #depending on the direction of the player's sprite
    def nearRight(self, walls):
        bool = False
        original_x = self.rect.x
        original_y = self.rect.y
        if(self.orientation == 'u'):
            self.rect.x += 50;    
        elif(self.orientation == 'l'):
            self.rect.y -= 50;
        elif(self.orientation == 'd'):
            self.rect.x -= 50;
        else:
            self.rect.y += 50;
            
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            bool = True
        #reset player's position back to normal
        self.rect.x = original_x
        self.rect.y = original_y
        return bool
    
    #method checks if there is a wall by the player's frontside
    #depending on the direction of the player's sprite
    def nearFront(self, walls):
        bool = False
        original_x = self.rect.x
        original_y = self.rect.y
        if(self.orientation == 'u'):
            self.rect.y -= 50;    
        elif(self.orientation == 'l'):
            self.rect.x -= 50;
        elif(self.orientation == 'd'):
            self.rect.y += 50;
        else:
            self.rect.x += 50;
            
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            bool = True
        #reset player's position back to normal
        self.rect.x = original_x
        self.rect.y = original_y
        return bool
    
    #moves player up one spot
    def moveUp(self, walls):
        self.rect.y -= 50
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            self.rect.y += 50
        else:
            self.rect.y -= 50
            self.actualY -= 100  
      
    #moves player left one spot            
    def moveLeft(self, walls):
        self.rect.x -= 50
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            self.rect.x += 50
        else:
            self.rect.x -= 50
            self.actualX -= 100
    
    #moves player down one spot 
    def moveDown(self, walls):
        self.rect.y += 50
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:      
            self.rect.y -= 50
        else:
            self.rect.y += 50
            self.actualY += 100
    
    #moves player right one spot              
    def moveRight(self, walls):
        self.rect.x += 50
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            self.rect.x -= 50
        else:
            self.rect.x += 50
            self.actualX += 100
             
    def resetOrientation(self):
        image = pygame.image.load("sprite3.png")
        image = pygame.transform.scale(image, (50,50))
        self.image = image
        self.orientation = 'u'
                  
class Room(object):
    """ Base class for all rooms. """
 
    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None
 
    def __init__(self):
       
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        

            
class EndScreen(Room):
    def __init__(self, maze_length):
        super().__init__()
        
        walls = [[0,0, (maze_length * 100) + 10,10,WHITE],
                 [0,10,10,(maze_length * 100) + 10,WHITE],
                 [10,(maze_length * 100) + 10,(maze_length * 100) + 10,10,WHITE],
                 [(maze_length * 100) + 10,0,10,(maze_length * 100) + 10,WHITE]]
        for item in walls:
            self.wall_list.add(Wall(item[0],item[1],item[2],item[3],item[4]))
     
def main():
    pygame.init()
    
    ser = serial.Serial("COM4", 57600)
    
    #loading image from directory and then scaling it to sprite size
    image = pygame.image.load("sprite3.png")
    image = pygame.transform.scale(image, (50,50))
    
    n = int(input("Define the size, n (n must be an integer greater than 1), for the n x n maze, n = "))
    random_x = 2#random.randint(0, n - 1)
    starting_x = 35 + (random_x*100)
    starting_y = ((n - 1) * 100) + 35
    
    bg = pygame.image.load("background.png")
    
    player = Player(starting_x, starting_y, image) #increment x by 100 to move player along last row in maze
    player.actualX = starting_x
    player.actualY = starting_y
    total_width = (n * 100) + 20
    total_height = (n * 100) + 20
    
    pygame.display.set_caption('Maze')
   
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    
    
    maze = MazeDatabase.StackMaze(n, random_x, n - 1)
    
    room_list = []
    room_list.append(maze)
    current_room = room_list[0]
    
    if(n < 7):
        screen = pygame.display.set_mode([(n * 100) + 20, (n * 100) + 20]) #increment x and y by 100 to change size of maze, do this to borders as well      
        end = EndScreen(n)
        bg = pygame.transform.scale(bg, ((n * 100) + 20,(n * 100) + 20))
    else:
        screen = pygame.display.set_mode([620,620])
        end = EndScreen(6)
        bg = pygame.transform.scale(bg, ((6 * 100) + 20,(6 * 100) + 20))
        player.rect.y = total_height - (total_height - 535)
        
        for wall in current_room.wall_list:
            wall.rect.y -= (player.actualY - player.rect.y)
        
        if(starting_x >= 435):
            
            if(starting_x > (total_width - 200)):
                player.rect.x = starting_x - (total_width - 620)
                for wall in current_room.wall_list:
                    wall.rect.x -= (total_width - 620)  
            elif(starting_x >= 435):
                player.rect.x = 335
                for wall in current_room.wall_list:
                    wall.rect.x -= (starting_x - 335)                       
            else:
                player.rect.x = 335
                for wall in current_room.wall_list:
                    wall.rect.x -= (player.actualX - player.rect.x)
            
    room_list.append(end)
    clock = pygame.time.Clock()
    done = False
       
    location = ''
    #before the game starts, user is given initial queues about where he is
    if(player.nearLeft(current_room.wall_list)):
        location = location + '1'
    else:
        location = location + '0'
        
    if(player.nearFront(current_room.wall_list)):
        location = location + '1'
    else:
        location = location + '0'
        
    if(player.nearRight(current_room.wall_list)):
        location = location + '1'
    else:
        location = location + '0'
        
    ser.write(str(int(location,2)).encode())
        
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #left key rotates player 90 degrees to the left
                    player.image = pygame.transform.rotate(player.image, 90)
                    if(player.orientation == 'u'):
                        player.orientation = 'l'
                    elif(player.orientation == 'l'):
                        player.orientation = 'd'
                    elif(player.orientation == 'd'):
                        player.orientation = 'r'
                    else:
                        player.orientation = 'u'         
                    
                if event.key == pygame.K_RIGHT:
                    #right key rotates player 90 degrees to the right
                    player.image = pygame.transform.rotate(player.image, -90)
                    if(player.orientation == 'u'):
                        player.orientation = 'r'
                    elif(player.orientation == 'l'):
                        player.orientation = 'u'
                    elif(player.orientation == 'd'):
                        player.orientation = 'l'
                    else:
                        player.orientation = 'd'     
                if event.key == pygame.K_UP:
                    #up key moves player forward one spot depending on direction of sprite
                    if(n < 7):
                        if(player.orientation == 'u'):
                            player.moveUp(current_room.wall_list)
                        elif(player.orientation == 'l'):
                            player.moveLeft(current_room.wall_list)
                        elif(player.orientation == 'd'):
                            player.moveDown(current_room.wall_list)
                        else:
                            player.moveRight(current_room.wall_list)
                    else:
                        
                        if(player.orientation == 'u'):
                            if((player.actualY > 300  and player.actualY < total_height - 320) and 
                               not player.nearFront(current_room.wall_list)):
                                player.actualY -= 100
                                for wall in current_room.wall_list:
                                    wall.rect.y += 100
                            else:
                                player.moveUp(current_room.wall_list)
                        elif(player.orientation == 'l'):
                            if((player.actualX > 400  and player.actualX < total_width - 220) and 
                               not player.nearFront(current_room.wall_list)):
                                player.actualX -= 100
                                for wall in current_room.wall_list:
                                    wall.rect.x += 100
                            else:
                                player.moveLeft(current_room.wall_list)
                        elif(player.orientation == 'd'):
                            if((player.actualY > 200 and player.actualY < total_height - 420) and 
                               not player.nearFront(current_room.wall_list)):
                                player.actualY += 100
                                for wall in current_room.wall_list:
                                    wall.rect.y -= 100
                            else:
                                player.moveDown(current_room.wall_list)
                        else:
                            if((player.actualX > 300  and player.actualX < total_width - 320) and 
                               not player.nearFront(current_room.wall_list)):
                                player.actualX += 100
                                for wall in current_room.wall_list:
                                    wall.rect.x -= 100
                            else:
                                player.moveRight(current_room.wall_list)
                    
                if event.key == pygame.K_DOWN:
                    #down key resets player orientation
                    player.resetOrientation()
                if event.key == pygame.K_r:
                    #resets the player's location to where he/she started
                    #as well as resetting the orientation
                    player.rect.x = starting_x
                    player.rect.y = starting_y
                    player.resetOrientation()
                '''
                for sprite in movingsprites:
                    
                    sprite.rect.x += 100
                    sprite.rect.y -= 100
         
                for sprite in current_room.wall_list:
                     
                    sprite.rect.x += 100
                    sprite.rect.y -= 100
                '''    
                #turn off all buzzers real briefly
                ser.write("0".encode())
                
                location = ''
                
                #depending on the location of the player,
                #appropriate serial signals are sent to the Arduino
                if(player.nearLeft(current_room.wall_list)):
                    location = location + '1'
                else:
                    location = location + '0'
        
                if(player.nearFront(current_room.wall_list)):
                    location = location + '1'
                else:
                    location = location + '0'
        
                if(player.nearRight(current_room.wall_list)):
                    location = location + '1'
                else:
                    location = location + '0'
        
                ser.write(str(int(location,2)).encode()) 
                
                #short delay between moves
                now = time.time()
                future = now + .002
                while time.time() < future:
                    pass #dummy statement
                
        #screen.fill(BLACK)
        screen.blit(bg, (0,0)) 
        
        #when the player finds the exit to the maze, the game ends with a winning screen
        if player.rect.y < 0 or player.rect.x > (n * 100) + 20 or player.rect.x < 0 or player.rect.y > (n * 100) + 20:
            current_room = room_list[1]
            
            if(n < 7):
                myfont = pygame.font.SysFont("monospace", n * 12)

                #render text
                label = myfont.render("You Won!", 1, BLUE)
                screen.blit(label, (15 * (n ** 1.25), 15 * (n ** 1.25)))
            else:
                myfont = pygame.font.SysFont("monospace", 6 * 12)

                #render text
                label = myfont.render("You Won!", 1, BLUE)
                screen.blit(label, (15 * (6 ** 1.25), 15 * (6 ** 1.25)))
            #movingsprites.remove(player)
            #player.kill()
        
        #camera.update(player)
        
                 
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(60)
    
    ser.write("0".encode())
    pygame.QUIT
if __name__ == "__main__":
    main()