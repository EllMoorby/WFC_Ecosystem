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
    def __init__(self,position,world):
        self.position = position
        self.energy = BASE_ENERGY
        self.urgeReproduce = URGE_REPRODUCE
        self.world = []

        for index,row in enumerate(world):
            self.world.append([])
            for cell in row:
                self.world[index].append(CreatureCell(cell.position,cell.tile))

    def ChooseOption(self):
        return random.choices(["ENERGY","REPRODUCE"],weights=[BASE_ENERGY-self.energy,URGE_REPRODUCE-self.urgeReproduce])
        pass

    def AdvancePath(self):
        self.position = self.currentpath.stack[0]
        self.currentpath.RemoveFromStack()
        if len(self.currentpath.stack) == 0: self.currentpath = None

    def Update(self,world,renderer):
        if self.currentpath is not None:
            self.AdvancePath()
        else:
            self.ChooseOption()

    def Move(self,target,renderer,world):
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,self.world[16][12])
        pathfinder.InitiatePathfind()
        self.currentpath = pathfinder.path
        for cell in range(len(pathfinder.path.stack)):
            item = pathfinder.path.RemoveFromStack()
            print(item.position)
        print(pathfinder.path.stack)

        print("---------")
        

    def LocateMate(self,world,target):
        #choose mate
        self.Move(target,world)
        pass #find a suitable mate


class Predator(Creature):
    def __init__(self,position,img,world):
        super().__init__(position,world)
        self.img = img
        self.urgeHunt = URGE_HUNT

    def Hunt(self):
        pass #locate a nearby prey and hunt it

    def Update(self):
        pass

class PredatorFemale(Predator):
    def __init__(self,position,img,world):
        super().__init__(position,img,world)

class Prey(Creature):
    def __init__(self,position,img,world):
        super().__init__(position,world)
        self.img = img
        self.health = BASE_HEALTH


    def Update(self):
        pass

    def Forage(self):
        #locate berry bushes for the world
        pass

    def Flee(self):
        #run from the predator chasing
        pass


class PreyFemale(Prey):
    def __init__(self,position,img,world):
        super().__init__(position,img,world)

         


