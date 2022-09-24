from constants import *
import math

class Stack:
    def __init__(self):
        self.stack = [] #The stack itself
        self.size = -1 #size/top value of the stack

    def AddToStack(self,item): #add to the top of the stack
        self.stack.append(item)
        self.size += 1

    def RemoveFromStack(self): #remove from the top of the stack 
        if self.size != -1:
            item = self.stack[(len(self.stack)-1)]
            self.stack.remove(item)
            self.size -= 1
            return item
        else:return
    
    def __iter__(self): #calling itself returns the stack for ease of use
        return self.stack


class PathFinder:
    def __init__(self,creature,target):
        self.world = creature.world.copy() #get the world map in CreatureCells
        self.creature = creature.position
        self.target = target
        self.exploredcells = [] #A list of cells the program has explored
        self.path = Stack() #create a stack for the path to be stored
        self.PathFound = False #Bool of if the path has been found

    def GetDistanceBetween(self,item1,item2): #get distance between two objects
        #get the difference in y and difference in x
        dx = item1.position[0] - item2.position[0]
        dy = item1.position[1] - item2.position[1]
        #use pythagoras to find the distance between points
        return (math.sqrt(dx*dx + dy*dy))

    def DetermineFandHCost(self): #get the h_cost, g_cost, and f_cost from the distances to determine the best path
        #gets the f and h cost of every cell in the world
        for row in self.world:
            for cell in row:
                cell.g_cost = self.GetDistanceBetween(cell,self.creature) #get distance between each cell and creature
                cell.h_cost = self.GetDistanceBetween(cell,self.target) #get distance between each cell and target
                cell.f_cost = cell.h_cost + cell.g_cost #f_cost equivalent to both h_cost and g_cost. the effective "cost" of a cell, the lower the better
                if not(cell.tile.traversable): #adds a modifier to dissuade the use of "non traversable" cells.
                    cell.f_cost *= NONTRAVERSABLE_MOVEMENT_MODIFYER

    def Explore(self,position): #explore the cells around a position, but not off of the screen. it sets all the cell's cell.pointer around not previously explored to the centre cell it returns true if the target cell is found 
        #loop through cells around position
        for x in range(-1,2):
            for y in range(-1,2):
                if (position != [x,y] and (0 <= position[0]+x <= ((SCREENWIDTH // CELLSIZE)-1)) and (0 <= position[1]+y <= ((SCREENHEIGHT // CELLSIZE)-1))): #filter out cells that are outside the playable space or are the current position
                    if (position[0] + x,position[1] + y) != self.creature.position:
                        if self.world[position[0] + x][position[1] + y].pointer == None: #if the cells has not already been explored
                            self.world[position[0] + x][position[1] + y].pointer = self.world[position[0]][position[1]] #sets pointer to the position of the origin cell
                            self.exploredcells.append(self.world[position[0] + x][position[1] + y]) #add the newcell to exploredcells
                        if ((position[0] + x),(position[1] + y)) == self.target.position: #if the target has been found, return True
                            return True

        
    def GetLowestFCost(self): #finds the lowest f_cost within the exploredcells list
        lowest = 999999999
        for cell in self.exploredcells:
            if cell.f_cost <= lowest:
                lowest = cell.f_cost
                lowestcell = cell
        return lowestcell


 
    def PathFind(self): #recursive algorithm where the paths are expanded from the creature until the target is found

        #add to explored cells
        cell = self.GetLowestFCost() #finds the cell with the lowest cost
        self.exploredcells.remove(cell) #remove it from exploredcells
        if self.Explore(cell.position): #returns true if path was found, stopping condition
            self.target.pointer = cell
            self.PathFound = True
        elif not(self.PathFound): #recursion if path not found
            self.PathFind()
        else:return


    def GetPath(self): #translates the shortest path to a stack to be used
        cell = self.target
        self.path.AddToStack(cell) #add the cell to the stack
        while cell.position != self.creature.position: #while the path has not been found
            cell = cell.pointer #work the pointers back to find the path
            if cell.position != self.creature.position:
                self.path.AddToStack(cell) #add stack to cell


    def InitiatePathfind(self): #initiates the pathfind algorithm
        self.DetermineFandHCost()
        self.Explore(self.creature.position)
        self.PathFind() #start recursion
        if self.PathFound:
            self.GetPath() #find path from the cells.
        

