from constants import *
from pathfinder import PathFinder
import random
import math

class CreatureCell:
    def __init__(self,position,tile) -> None:
        self.position = (position[0],position[1])
        self.centreposition = [(self.position[0]*CELLSIZE)+CELLSIZE//2,(self.position[1]*CELLSIZE)+CELLSIZE//2]
        self.tile = tile
        self.g_cost = 0 #dist from start
        self.h_cost = 0 #dist from end
        self.f_cost = 0 #Gcost+Hcost
        self.pointer = None
        self.traversable = self.tile.traversable
        self.currentpath = None

class Creature:
    def __init__(self,position,world,renderer):
        self.position = position
        self.energy = BASE_ENERGY
        self.urgeReproduce = URGE_REPRODUCE
        self.worldmap = world
        self.currentpath = None
        self.renderer = renderer

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

    def ChooseOption(self):
        return random.choices(["ENERGY","REPRODUCE"],weights=[BASE_ENERGY-self.energy,URGE_REPRODUCE-self.urgeReproduce])

    def AdvancePath(self):
        try:
            self.position = self.currentpath.stack[self.currentpath.size]
            self.currentpath.RemoveFromStack()
            self.renderer.DrawCreature(self)
        except:return
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        
    def Update(self,berryList):
        if self.currentpath is not None:
            self.AdvancePath()
        else:
            target = self.Forage(berryList)
            self.FindPath(target)

    def FindPath(self,target):
        print(target)
        self.world = self.CreateCreatureWorld()
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,target)
        pathfinder.InitiatePathfind()
        self.currentpath = pathfinder.path

        print("---------")
        

    def LocateMate(self,world,target):
        #choose mate
        self.Move(target,world)
        pass #find a suitable mate


class Predator(Creature):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,world,renderer)
        self.img = img
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

class PredatorFemale(Predator):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,img,world,renderer)

class Prey(Creature):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,world,renderer)
        self.img = img
        self.hasPredator = False
        self.health = BASE_HEALTH


    def Forage(self,berryList):
        lowest = 99999999
        lowestberry = None
        for berry in berryList:
            dist = self.GetDistanceBetween(berry,self)
            if not(berry.hasTarget) and dist < lowest:
                lowest = dist
                lowestberry = berry
        lowestberryInCreatureWorld = self.world[lowestberry.position[0]][lowestberry.position[1]]
        lowestberryInCreatureWorld.hasTarget = True
        return lowestberryInCreatureWorld

    def Flee(self):
        #run from the predator chasing
        pass


class PreyFemale(Prey):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,img,world,renderer)

         


