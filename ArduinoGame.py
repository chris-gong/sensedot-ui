'''
Created on Jun 22, 2016

@author: Chris Gong
'''

import GameArea
#before adding external library path, above import statement would be
#from datatransfer import GameArea (replace "datatransfer" with package name)
import pygame
import serial

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.up = True
        self.image = image
        
        #self.image = pygame.Surface([50,50])
        #self.image.fill(GameArea.BLUE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def nearLeft(self, walls):
        bool = False
        self.rect.x -= 50;
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            bool = True
        self.rect.x += 50;
        return bool
        
    def nearRight(self, walls):
        bool = False
        self.rect.x += 50;
        block_hit_list = pygame.sprite.spritecollide(self,walls,False)
        if block_hit_list:
            bool = True
        self.rect.x -= 50;
        return bool
    
    def nearFront(self, walls):
        bool = False
        if(self.up):
            self.rect.y -= 50;
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                bool = True
            self.rect.y += 50;
        else:
            self.rect.y += 50;
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                bool = True
            self.rect.y -= 50;
        return bool
    
    def move(self, direction, walls):
        if(direction == "left"):
            self.rect.x -= 50
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                self.rect.x += 50
            else:
                self.rect.x -= 50
                
        elif(direction == "right"):
            self.rect.x += 50
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                self.rect.x -= 50
            else:
                self.rect.x += 50
         
        elif(direction == "up"):
            self.rect.y -= 50
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                self.rect.y += 50
            else:
                self.rect.y -= 50
        
        elif(direction == "down"):
            self.rect.y += 50
            block_hit_list = pygame.sprite.spritecollide(self,walls,False)
            if block_hit_list:
                self.rect.y -= 50
            else:
                self.rect.y += 50
                              

class Maze1(GameArea.Room):
    def __init__(self):
        super().__init__()
        walls = [[105,310,10,100,GameArea.WHITE],
                 [110,305,100,10,GameArea.WHITE],
                 [210,305,100,10,GameArea.WHITE],
                 [110,105,100,10,GameArea.WHITE],
                 [110,205,100,10,GameArea.WHITE],
                 [205,110,10,100,GameArea.WHITE],
                 [305,110,10,100,GameArea.WHITE],
                 [310,205,100,10,GameArea.WHITE],
                 [0,0,315,10,GameArea.WHITE],
                 [0,10,10,410,GameArea.WHITE],
                 [10,410,410,10,GameArea.WHITE],
                 [410,0,10,410,GameArea.WHITE]]
        for item in walls:
            self.wall_list.add(GameArea.Wall(item[0],item[1],item[2],item[3],item[4]))
            
class Maze2(GameArea.Room):
    def __init__(self):
        super().__init__()
        walls = [[110,105,100,10,GameArea.WHITE],
                 [110,205,100,10,GameArea.WHITE],
                 [205,10,10,100,GameArea.WHITE],
                 [205,210,10,100,GameArea.WHITE],
                 [210,205,100,10,GameArea.WHITE],
                 [305,110,10,100,GameArea.WHITE],
                 [305,310,10,100,GameArea.WHITE],
                 [310,205,100,10,GameArea.WHITE],
                 [0,0,315,10,GameArea.WHITE],
                 [0,10,10,410,GameArea.WHITE],
                 [10,410,410,10,GameArea.WHITE],
                 [410,0,10,410,GameArea.WHITE]]
        for item in walls:
            self.wall_list.add(GameArea.Wall(item[0],item[1],item[2],item[3],item[4]))
            
class Maze3(GameArea.Room):
    def __init__(self):
        super().__init__()
        
        walls = [[10,205,100,10,GameArea.WHITE],
                 [105,310,10,100,GameArea.WHITE],
                 [205,210,10,100,GameArea.WHITE],
                 [205,10,10,100,GameArea.WHITE],
                 [210,105,100,10,GameArea.WHITE],
                 [210,305,100,10,GameArea.WHITE],
                 [305,110,10,100,GameArea.WHITE],
                 [305,310,10,100,GameArea.WHITE],
                 [0,0,315,10,GameArea.WHITE],
                 [0,10,10,410,GameArea.WHITE],
                 [10,410,410,10,GameArea.WHITE],
                 [410,0,10,410,GameArea.WHITE]]
        for item in walls:
            self.wall_list.add(GameArea.Wall(item[0],item[1],item[2],item[3],item[4]))
class EndScreen(GameArea.Room):
    def __init__(self):
        super().__init__()
        
        walls = [[0,0,410,10,GameArea.WHITE],
                 [0,10,10,410,GameArea.WHITE],
                 [10,410,410,10,GameArea.WHITE],
                 [410,0,10,410,GameArea.WHITE]]
        for item in walls:
            self.wall_list.add(GameArea.Wall(item[0],item[1],item[2],item[3],item[4]))

def main():
    pygame.init()
    
    ser = serial.Serial("COM4", 57600)
    
    #loading image from directory and then scaling it to sprite size
    image = pygame.image.load("arrow.png")
    image = pygame.transform.scale(image, (50,50))
    
    
    
    player = Player(135,335, image)#increment x by 100 to move player along last row in maze
    screen = pygame.display.set_mode([420,420])         
    pygame.display.set_caption('Maze')
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    
    end = EndScreen()
    maze = Maze2()
    #maze = MazeDatabase.Maze2()
    room_list = []
    room_list.append(end)
    room_list.append(maze)
    current_room = room_list[1]
    
    clock = pygame.time.Clock()
    done = False
    
    #before the game starts, user is given initial queues about where he is
    if(player.nearLeft(current_room.wall_list)):
        ser.write("left".encode())
        clock.tick(60)
        ser.write("left".encode())
        clock.tick(60)
    if(player.nearRight(current_room.wall_list)):
        ser.write("right".encode())
        clock.tick(60)
        ser.write("right".encode())
        clock.tick(60)
    if(player.nearFront(current_room.wall_list)):
        ser.write("mid".encode())
        clock.tick(60)
        ser.write("mid".encode())
        clock.tick(60)
        
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move("left", current_room.wall_list)
                if event.key == pygame.K_RIGHT:
                    player.move("right", current_room.wall_list)
                if event.key == pygame.K_UP:
                    #up arrow moves player forward depending on direction of sprite
                    if(player.up):
                        player.move("up", current_room.wall_list)
                    else:
                        player.move("down", current_room.wall_list)
                if event.key == pygame.K_DOWN :
                    #down key rotates sprite image
                    player.image = pygame.transform.rotate(player.image, 180)
                    player.up = not player.up
                
                #turn off all buzzers real briefly
                ser.write("off".encode())
                clock.tick(60)
                ser.write("off".encode())
                clock.tick(60)
                
                if(player.nearLeft(current_room.wall_list)):
                    ser.write("left".encode())
                    clock.tick(60)
                    ser.write("left".encode())
                    clock.tick(60)
                if(player.nearRight(current_room.wall_list)):
                    ser.write("right".encode())
                    clock.tick(60)
                    ser.write("right".encode())
                    clock.tick(60)
                if(player.nearFront(current_room.wall_list)):
                    ser.write("mid".encode())
                    clock.tick(60)
                    ser.write("mid".encode())
                    clock.tick(60)
                
        screen.fill(GameArea.BLACK)
        
        if player.rect.y < 0 or player.rect.x > 420 or player.rect.x < 0 or player.rect.y > 420:
            current_room = room_list[0]
            
            myfont = pygame.font.SysFont("monospace", 50)

            #render text
            label = myfont.render("You Won!", 1, GameArea.WHITE)
            screen.blit(label, (100, 100))
            #movingsprites.remove(player)
            #player.kill()
            
            
                
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(60)
    
    pygame.QUIT
if __name__ == "__main__":
    main()