from os import remove
from secrets import choice
from tkinter.tix import CELL
from constants import *
from pathfinder import PathFinder,Stack
import random
import math
import pygame


class CreatureCell:
    def __init__(self,position,tile) -> None:
        self.position = (position[0],position[1])
        self.tile = tile
        self.g_cost = 0 #dist from start
        self.h_cost = 0 #dist from end
        self.f_cost = 0 #Gcost+Hcost
        self.pointer = None
        self.traversable = self.tile.traversable

class Creature:
    def __init__(self,position,world,renderer):
        self.position = position
        self.energy = BASE_ENERGY
        self.urgeReproduce = URGE_REPRODUCE
        self.worldmap = world
        self.currentpath = Stack()
        self.renderer = renderer
        self.count = 0
        self.foodTarget = None
        self.mate = None
        

        self.world = self.CreateCreatureWorld()

    def GetDistanceBetween(self,item1,item2):
        dx = item1.position[0] - item2.position[0]
        dy = item1.position[1] - item2.position[1]
        return math.sqrt(dx*dx + dy*dy)


    def CreateCreatureWorld(self):
        world = []
        for index,row in enumerate(self.worldmap):
            world.append([])
            for cell in row:
                world[index].append(CreatureCell(cell.position,cell.tile))

        return world

    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        self.position = self.currentpath.stack[self.currentpath.size]
        self.currentpath.RemoveFromStack()
        if self.foodTarget and self.foodTarget.position == self.position.position:
            self.energy += BERRYENERGYREFILL
            return True
        
        self.energy -= LOSSPERSTEP
        return False
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        

    def FindPath(self,target):
        self.world = self.CreateCreatureWorld()
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,target)
        pathfinder.InitiatePathfind()
        currentpath = pathfinder.path
        
        return currentpath
        

    def LocateMate(self,preyLookingForMate):
        pass

    def Wander(self,spawnableList):
        possibleWanderTiles = []
        for item in spawnableList:
            if self.GetDistanceBetween(self.position,item) <= MAXWANDERDISTANCE and item.position != self.position.position:
                possibleWanderTiles.append(item)

        cell = random.choice(possibleWanderTiles)
        cell = self.world[cell.position[0]][cell.position[1]]
        return cell


class Predator(Creature):
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"fox.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.urgeHunt = URGE_HUNT

    def Hunt(self,preyList):
        lowest = 99999999
        lowestprey = None
        for prey in preyList:
            dist = self.GetDistanceBetween(prey,self)
            if not(prey.hasTarget) and dist < lowest:
                lowest = dist
                lowestprey = prey
        lowestpreyInCreatureWorld = self.world[lowestprey.position[0]][lowestprey.position[1]]
        lowestpreyInCreatureWorld.hasPredator = True
        return lowestpreyInCreatureWorld

    def Update(self):
        pass

class Prey(Creature):
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"rabbit.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.hasPredator = False
        self.health = BASE_HEALTH
        self.lookingForMate = False
        

    def Update(self,berryList,fertileList,spawnableList,preyLookingForMate):
        if self.energy <= 0:
            return -1
        if len(self.currentpath.stack) == 0:
            self.foodTarget = None
            option = self.ChooseActivity()
            match option[0]:
                case "f":
                    pass
                case "e":
                    target = self.Forage(berryList)
                    if target == -1:
                        target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "w":
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r":
                    pass
        else:
            removeberry = self.AdvancePath()
            if removeberry:
                berryList.remove(self.foodTarget)

        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS
        if self.hasPredator:
            return "f"

        choiceweights[0] += (BASE_ENERGY-self.energy) #eat chance
        choiceweights[1] += (self.energy/BASE_ENERGY + self.urgeReproduce/URGE_REPRODUCE)/2 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE-self.urgeReproduce) #chance to reproduce
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        return random.choices(["e","w","r"],choiceweights,k=1)

    def Forage(self,berryList):
        lowest = 99999999
        lowestberry = None
        for berry in berryList:
            dist = self.GetDistanceBetween(berry,self.position)
            if not(berry.hasTarget) and dist < lowest:
                lowest = dist
                lowestberry = berry
        if lowestberry == None:
            return -1
        self.foodTarget = lowestberry
        lowestberry.hasTarget = True
        lowestberryInCreatureWorld = self.world[lowestberry.position[0]][lowestberry.position[1]]
        return lowestberryInCreatureWorld

    def Flee(self):
        #run from the predator chasing
        pass


         


