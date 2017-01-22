'''
Created on Jul 1, 2016

@author: Chris Gong
'''
#Replace "datatransfer" with package name

import ArduinoMaze
import Stack

class Maze1(ArduinoMaze.Room):
    def __init__(self):
        super().__init__()
        #when doing circular importing with modules, objects cannot
        #extend imported class and its variables, change the ArduinoMaze.Room to object,
        #uncomment the line below, and run this file to see why
        #r = ArduinoMaze.Room
        walls = [[105,310,10,100,ArduinoMaze.WHITE],
                 [110,305,100,10,ArduinoMaze.WHITE],
                 [210,305,100,10,ArduinoMaze.WHITE], 
                 [110,105,100,10,ArduinoMaze.WHITE],
                 [110,205,100,10,ArduinoMaze.WHITE],
                 [205,110,10,100,ArduinoMaze.WHITE],
                 [305,110,10,100,ArduinoMaze.WHITE],
                 [310,205,100,10,ArduinoMaze.WHITE],
                 [0,0,315,10,ArduinoMaze.WHITE],
                 [0,10,10,410,ArduinoMaze.WHITE],
                 [10,410,410,10,ArduinoMaze.WHITE],
                 [410,0,10,410,ArduinoMaze.WHITE]]
        for item in walls:
            self.wall_list.add(ArduinoMaze.Wall(item[0],item[1],item[2],item[3],item[4]))
            
class Maze2(ArduinoMaze.Room):
    def __init__(self):
        super().__init__()
        walls = [[110,105,100,10,ArduinoMaze.WHITE],
                 [110,205,100,10,ArduinoMaze.WHITE],
                 [205,10,10,100,ArduinoMaze.WHITE],
                 [205,210,10,100,ArduinoMaze.WHITE],
                 [210,205,100,10,ArduinoMaze.WHITE],
                 [305,110,10,100,ArduinoMaze.WHITE],
                 [305,310,10,100,ArduinoMaze.WHITE],
                 [310,205,100,10,ArduinoMaze.WHITE],
                 [0,0,315,10,ArduinoMaze.WHITE],
                 [0,10,10,410,ArduinoMaze.WHITE],
                 [10,410,410,10,ArduinoMaze.WHITE],
                 [410,0,10,410,ArduinoMaze.WHITE]]
        for item in walls:
            self.wall_list.add(ArduinoMaze.Wall(item[0],item[1],item[2],item[3],item[4]))
            
class Maze3(ArduinoMaze.Room):
    def __init__(self):
        super().__init__()
        
        walls = [[10,205,100,10,ArduinoMaze.WHITE],
                 [105,310,10,100,ArduinoMaze.WHITE], 
                 [205,210,10,100,ArduinoMaze.WHITE],
                 [205,10,10,100,ArduinoMaze.WHITE],
                 [210,105,100,10,ArduinoMaze.WHITE],
                 [210,305,100,10,ArduinoMaze.WHITE],
                 [305,110,10,100,ArduinoMaze.WHITE],
                 [305,310,10,100,ArduinoMaze.WHITE],
                 [0,0,315,10,ArduinoMaze.WHITE],
                 [0,10,10,410,ArduinoMaze.WHITE],
                 [10,410,410,10,ArduinoMaze.WHITE],
                 [410,0,10,410,ArduinoMaze.WHITE]]
        for item in walls:
            self.wall_list.add(ArduinoMaze.Wall(item[0],item[1],item[2],item[3],item[4]))
            
class StackMaze(ArduinoMaze.Room):
    
    def __init__(self, maze_length, x, y):
        super().__init__()
        
        cellStack = Stack.CellStack(maze_length)
        cellStack.makeMaze(x, y)
        
        for x in range(0, maze_length):
            for y in range(0, maze_length):
                for item in cellStack.cell_list[x][y].hor_wall_list:
                    self.wall_list.add(item)
                for item in cellStack.cell_list[x][y].ver_wall_list:
                    self.wall_list.add(item)
        

        '''
        Below are the borders of the maze to ensure that 
        the topmost rightmost corner is open
        '''            
        walls = [[0,0, (y * 100) + 15,10,ArduinoMaze.WHITE],
                 [0,10,10,(maze_length * 100) + 10,ArduinoMaze.WHITE],
                 [10,(maze_length * 100) + 10,(maze_length * 100) + 10,10,ArduinoMaze.WHITE],
                 [(maze_length * 100) + 10,0,10,(maze_length * 100) + 10,ArduinoMaze.WHITE]]
                
        for item in walls:
            self.wall_list.add(ArduinoMaze.Wall(item[0],item[1],item[2],item[3],item[4]))