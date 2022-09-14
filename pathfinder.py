from turtle import pos, position
from constants import *
import math
from random import choice

class Stack:
    def __init__(self):
        self.stack = []

    def AddToStack(self,item):
        self.stack.append(item)

    def RemoveFromStack(self):
        item = self.stack[(len(self.stack)-1)]
        self.stack.remove(item)
        return item

class PathFinder:
    def __init__(self,creature,target):
        self.world = creature.world
        self.creature = creature
        self.target = target
        self.creaturecentre = [(self.creature.position[0]*CELLSIZE)+CELLSIZE//2,(self.creature.position[1]*CELLSIZE)+CELLSIZE//2]
        self.targetcentre = [(self.target.position[0]*CELLSIZE)+CELLSIZE//2,(self.target.position[1]*CELLSIZE)+CELLSIZE//2]
        self.exploredcells = []
        self.path = Stack()
        self.PathFound = False

    def GetDistanceBetween(self,item1,item2):
        dx = item1.position[0] - item2.position[0]
        dy = item1.position[1] - item2.position[1]

        return round((math.sqrt(dx*dx + dy*dy)),0)

    def DetermineFandHCost(self):
        for row in self.world:
            for cell in row:
                cell.g_cost = self.GetDistanceBetween(cell,self.creature)
                cell.h_cost = self.GetDistanceBetween(cell,self.target) #Must update to target.position
                cell.f_cost = cell.h_cost + cell.g_cost

    def Explore(self,position):
        for x in range(-1,2):
            for y in range(-1,2):
                if (position != [x,y] and (0 <= position[0]+x <= ((SCREENWIDTH // CELLSIZE)-1)) and (0 <= position[1]+y <= ((SCREENHEIGHT // CELLSIZE)-1))):
                    if self.world[position[0] + x][position[1] + y].traversable and (position[0] + x,position[1] + y) != self.creature.position:
                        if self.world[position[0] + x][position[1] + y] not in self.exploredcells:
                            self.world[position[0] + x][position[1] + y].pointer = self.world[position[0]][position[1]]
                            self.exploredcells.append(self.world[position[0] + x][position[1] + y])
                        if ((position[0] + x),(position[1] + y)) == self.target.position:
                            return True

        
    def GetLowestFCost(self):
        lowest = 999999999999999
        lowlist = []
        for cell in self.exploredcells:
            if cell.f_cost <= lowest:
                lowest = cell.f_cost

        for cell in self.exploredcells:
            if lowest == cell.f_cost:
                lowlist.append(cell)
                

        item = choice(lowlist)
        return item


 
    def PathFind(self):

        #add to explored cells
        cell = self.GetLowestFCost()
        
        if self.Explore(cell.position):
            self.world[self.target.position[0]][self.target.position[1]].pointer = cell
            self.PathFound = True
        elif not(self.PathFound):
            self.PathFind()
        else:return


    def GetPath(self):
        cell = self.target
        self.path.AddToStack(cell)
        while cell.position != self.creature.position:
            cell = cell.pointer
            if cell.position != self.creature.position:
                self.path.AddToStack(cell)


    def InitiatePathfind(self):
        self.DetermineFandHCost()
        self.Explore(self.creature.position)
        self.PathFind()
        if self.PathFound:
            self.GetPath()
        

