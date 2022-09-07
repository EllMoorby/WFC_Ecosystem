from constants import *

class Creature:
    def __init__(self):
        self.energy = BASEENERGY
        self.urgeReproduce = URGEREPRODUCE

class Predator(Creature):
    def __init__(self):
        Creature.__init__(self)
        self.urgeHunt = URGEHUNT

class Prey(Creature):
    def __init__(self):
        Creature.__init__(self)
         


