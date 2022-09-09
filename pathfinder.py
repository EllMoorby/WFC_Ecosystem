from constants import *
import math

class PathFinder:
    def __init__(self,world,creature,target):
        self.world = world.copy()
        self.creature = creature
        self.target = target
        self.creaturecentre = [(self.creature.position[0]*CELLSIZE)+CELLSIZE//2,(self.creature.position[1]*CELLSIZE)+CELLSIZE//2]
        self.targetcentre = [(self.target.position[0]*CELLSIZE)+CELLSIZE//2,(self.target.position[1]*CELLSIZE)+CELLSIZE//2]


    def GetDistanceBetween(self,item1pos,item2pos):
        dx = abs(item1pos[0] - item2pos[0])
        dy = abs(item1pos[1] - item2pos[1])

        return math.sqrt(dx*dx + dy*dy)

    def CheckNeighbors(self,position):
        neighbourlist = []
        for x in range(-1,2):
            for y in range(-1,2):
                if position != [x,y] and (0 <= position[0]+x <= ((SCREENWIDTH // CELLSIZE)-1)) and (0 <= position[1]+y <= ((SCREENHEIGHT // CELLSIZE)-1)):
                    neighbourlist.append([position[0] + x, position[1] + y])

        return neighbourlist


    def DetermineFandHCost(self):
        for row in self.world:
            for cell in row:
                cell.GetDistanceBetween() #need to either make a copy of world to assign dist to each cell


    def PathFind(self):
        pass


