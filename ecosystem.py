from constants import *
from pathfinding import PathFind

class Creature:
    def __init__(self,position):
        self.position = position
        self.energy = BASEENERGY
        self.urgeReproduce = URGEREPRODUCE


    def Update(self,world,renderer):
        #choose the best action to perform
        #carry out action, 1 turn at a time
        pass

    def Move(self,target,renderer,world):
        #move towards target, otherwise create a random target position

        PathFind(self,target,world)
        self.position[0] += 1
        renderer.DrawCreature(self)
        
        pass 

    def LocateMate(self,world,target):
        #choose mate
        self.Move(target,world)
        pass #find a suitable mate


class Predator(Creature):
    def __init__(self,position,img):
        super().__init__(position)
        self.img = img
        self.urgeHunt = URGEHUNT

    def Hunt(self):
        pass #locate a nearby prey and hunt it

    def Update(self):
        pass

class PredatorFemale(Predator):
    def __init__(self,position,img):
        super().__init__(position,img)

class Prey(Creature):
    def __init__(self,position,img):
        super().__init__(position)
        self.img = img
        self.health = BASEHEALTH

    def Forage(self):
        pass

    def Update(self):
        pass

class PreyFemale(Prey):
    def __init__(self,position,img):
        super().__init__(position,img)

         


