'''
Created on Jul 14, 2016

@author: Chris Gong
'''

import ArduinoMaze
import random

class Cell(object):
    def __init__(self, x, y):
        self.hor_wall_list = []
        self.ver_wall_list = []
        self.neighboring_cells = []
        self.row = x
        self.col = y
    
class Stack(object):
    
    def __init__(self, maze_length):
        self.maze_length = maze_length
        self.cell_list = [[0 for x in range(maze_length)] for y in range(maze_length)]
        self.all_hor_walls = [[0 for x in range(maze_length)] for y in range(maze_length-1)]
        self.all_ver_walls = [[0 for x in range(maze_length-1)] for y in range(maze_length)]
        self.stack = []
        
    def pop(self):
        if(len(self.stack) > 0):
            return self.stack.pop()
        
    def insert(self, cell):
        self.stack.append(cell)
        
    def peek(self):
        return self.stack[-1]
    
    def isEmpty(self):
        return len(self.stack)== 0

class CellStack(Stack):
    
    def __init__(self, maze_length):
        super().__init__(maze_length)
        #creating cell list
        for x in range(0, maze_length):
            for y in range(0, maze_length):
                self.cell_list[x][y] = Cell(x,y)
        
        #cells with two walls
        for x in range(0, 1):
            for y in range(0, 1):
                self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
            for y in range(maze_length - 1, maze_length):
                self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
        
        for x in range(maze_length - 1, maze_length):
            for y in range(maze_length - 1, maze_length):
                self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
        
            for y in range(0, 1):
                self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
        for x in range(0,1):
            for y in range(0, 1):
                self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
        
            for y in range(maze_length - 1, maze_length):
                self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                
        for x in range(maze_length - 1, maze_length):
            for y in range(maze_length - 1, maze_length):
                self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                
            for y in range(0, 1):
                self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
        #cells with 3 walls, if any
        if(maze_length > 2):
            for x in range(1, maze_length - 1):
                for y in range(0, 1):
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
            
            for x in range(1, maze_length - 1):
                for y in range(maze_length - 1, maze_length):
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
            
            for x in range(0, 1):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
            
            for x in range(maze_length - 1, maze_length):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
        
             
        #cells with 4 walls, if any
        if(maze_length > 2):      
            for x in range(1,maze_length - 1):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 5, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].hor_wall_list.append(ArduinoMaze.Wall((y*100)+10, (maze_length-1) * 100 - 
                                                        (x * 100) + 105, 100, 10, ArduinoMaze.WHITE))
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+105, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))    
                    self.cell_list[x][y].ver_wall_list.append(ArduinoMaze.Wall((y*100)+5, (maze_length-1) * 100 - 
                                                        (x * 100) + 10, 10, 100, ArduinoMaze.WHITE))
        
        #establishing neighbors
        #corner cells with only two neighbors
        self.cell_list[0][0].neighboring_cells.append(self.cell_list[0][1])
        self.cell_list[0][0].neighboring_cells.append(self.cell_list[1][0])
          
        self.cell_list[maze_length - 1][0].neighboring_cells.append(self.cell_list[maze_length - 2][0])
        self.cell_list[maze_length - 1][0].neighboring_cells.append(self.cell_list[maze_length - 1][1])
        
        self.cell_list[0][maze_length - 1].neighboring_cells.append(self.cell_list[1][maze_length - 1])
        self.cell_list[0][maze_length - 1].neighboring_cells.append(self.cell_list[0][maze_length - 2])
        
        self.cell_list[maze_length - 1][maze_length - 1].neighboring_cells.append(self.cell_list[maze_length - 2][maze_length - 1])
        self.cell_list[maze_length - 1][maze_length - 1].neighboring_cells.append(self.cell_list[maze_length - 1][maze_length - 2])
        
        #cells with three neighbors
        if(maze_length > 2):
            for x in range(1,maze_length - 1):
                for y in range(0, 1):
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x + 1][y])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x - 1][y])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y + 1])
                    
            for x in range(1,maze_length - 1):
                for y in range(maze_length - 1, maze_length):
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x + 1][y])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x - 1][y])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y - 1])
                    
            for x in range(0, 1):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y - 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y + 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x + 1][y])
            
            for x in range(maze_length - 1, maze_length):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y - 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y + 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x - 1][y])
                    
        #cells with 4 neighbors
            for x in range(1,maze_length - 1):
                for y in range(1, maze_length - 1):
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y - 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x][y + 1])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x - 1][y])
                    self.cell_list[x][y].neighboring_cells.append(self.cell_list[x + 1][y])
                    
        
                    
    def makeMaze(self, start_x, start_y):
        current = self.cell_list[0][start_x]
        
        visited = [[0 for x in range(self.maze_length)] for y in range(self.maze_length)]
        visited[0][start_x] = True
        self.insert(current)
        
        while not self.isEmpty():
            top = self.peek()
            current = top #this was the key to fixing this because I would set current to the top on
            #the way back up the stack but top would equal the one after current in the stack
            #but top is what's used to find neighbors while current would be used to find similar walls
            hasUnvisited = False
            s = set()
            count = 0
            
            while len(s) < len(top.neighboring_cells):
                s.add(count)
                count = count + 1
                
            num = random.randint(0, len(s) - 1)
            neighbor = top.neighboring_cells[list(s)[num]]
            
            while visited[neighbor.row][neighbor.col] and len(s) > 1:
                num = random.randint(0, len(s) - 1)
                neighbor = top.neighboring_cells[list(s)[num]]
                s.remove(list(s)[num])
            
            if(len(s) == 1 and visited[neighbor.row][neighbor.col]):
                num = list(s)[0]
                neighbor = top.neighboring_cells[num]
                if not visited[neighbor.row][neighbor.col]:
                    hasUnvisited = True
            else:
                if not visited[neighbor.row][neighbor.col]:
                    hasUnvisited = True
            
            if(hasUnvisited):

                condToBreakOut1 = False
                condToBreakOut2 = False
                
                for x in range(0, len(current.hor_wall_list)):
                    for y in range(0, len(neighbor.hor_wall_list)):
                        if(current.hor_wall_list[x].equals(neighbor.hor_wall_list[y])):
                            del current.hor_wall_list[x]
                            del neighbor.hor_wall_list[y]
                            
                            condToBreakOut1 = True
                            break
                    if(condToBreakOut1):
                        break       
                for x in range(0, len(current.ver_wall_list)):
                    for y in range(0, len(neighbor.ver_wall_list)):
                        if(current.ver_wall_list[x].equals(neighbor.ver_wall_list[y])):
                            del current.ver_wall_list[x]
                            del neighbor.ver_wall_list[y]
                            
                            condToBreakOut2 = True
                            break
                    if(condToBreakOut2):
                        break
                
                     
                current = neighbor
                self.insert(current)
                visited[current.row][current.col] = True
                   
            
                
            elif(not self.isEmpty()):
                cell = self.pop()
                current = cell
                
                
                

        