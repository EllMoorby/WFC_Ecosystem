from constants import *

class Creature:
    def __init__(self,position):
        self.position = position
        self.energy = BASEENERGY
        self.urgeReproduce = URGEREPRODUCE

    def Move(self,target):
        pass #move towards target, otherwise create a random target position

    def LocateMate(self):
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

         


