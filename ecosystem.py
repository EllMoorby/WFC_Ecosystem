from constants import *
from pathfinder import PathFinder
class CreatureCell:
    def __init__(self,position,tile) -> None:
        self.position = position
        self.centreposition = [(self.position[0]*CELLSIZE)+CELLSIZE//2,(self.position[1]*CELLSIZE)+CELLSIZE//2]
        self.tile = tile
        self.g_cost = 0 #dist from start
        self.h_cost = 0 #dist from end
        self.f_cost = 0 #Gcost+Hcost
        self.pointer = None
        self.traversable = self.tile.traversable

class Creature:
    def __init__(self,position,world):
        self.position = position
        self.energy = BASEENERGY
        self.urgeReproduce = URGEREPRODUCE
        self.world = []

        for index,row in enumerate(world):
            self.world.append([])
            for cell in row:
                self.world[index].append(CreatureCell(cell.position,cell.tile))

    def Update(self,world,renderer):
        #choose the best action to perform
        #carry out action, 1 turn at a time
        pass

    def Move(self,target,renderer,world):
        #move towards target, otherwise create a random target position
        testpathfinder = PathFinder(self,self.world[4][0])
        testpathfinder.InitiatePathfind()
        for item in testpathfinder.path:
            print(item.position)

        print("---------")
        

    def LocateMate(self,world,target):
        #choose mate
        self.Move(target,world)
        pass #find a suitable mate


class Predator(Creature):
    def __init__(self,position,img,world):
        super().__init__(position,world)
        self.img = img
        self.urgeHunt = URGEHUNT

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
        self.health = BASEHEALTH


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

         


