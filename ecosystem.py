import re
from constants import *
from pathfinder import PathFinder
import random

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

        self.CreateCreatureWorld()


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
        
        

    def Update(self):
        if self.currentpath is not None:
            self.AdvancePath()
        else:
            #self.ChooseOption()
            self.FindPath((random.randint(0,(SCREENWIDTH//CELLSIZE)-1),random.randint(0,(SCREENHEIGHT//CELLSIZE)-1)))

    def FindPath(self,target):
        self.world = self.CreateCreatureWorld()
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,self.world[target[0]][target[1]])
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

    def Hunt(self):
        pass #locate a nearby prey and hunt it

    def Update(self):
        pass

class PredatorFemale(Predator):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,img,world,renderer)

class Prey(Creature):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,world,renderer)
        self.img = img
        self.health = BASE_HEALTH


    def Forage(self):
        #locate berry bushes for the world
        pass

    def Flee(self):
        #run from the predator chasing
        pass


class PreyFemale(Prey):
    def __init__(self,position,img,world,renderer):
        super().__init__(position,img,world,renderer)

         


