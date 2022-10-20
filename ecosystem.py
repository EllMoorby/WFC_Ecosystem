from constants import *
from pathfinder import PathFinder,Stack
import random
import math
import pygame

class Queue:
    def __init__(self):
        self.fPointer = 0
        self.rPointer = -1
        self.list = []

    def AddToQueue(self,item):
        self.rPointer += 1
        self.list.append(item)

    def RemoveFromQueue(self):
        if self.fPointer <= self.rPointer:
            item = self.list[self.fPointer]
            self.list.pop(self.fPointer)
            self.rPointer-=1
            return item

    def ClearQueue(self):
        self.fPointer = 0
        self.rPointer = -1
        self.list = []

    def BackOfQueue(self):
        if self.fPointer <= self.rPointer:
            return self.list[self.rPointer]
        return
    


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
    def __init__(self,position,world,renderer,cellsize):
        self.CELLSIZE = cellsize
        self.position = position
        self.worldmap = world
        self.currentpath = Stack()
        self.renderer = renderer
        self.foodTarget = None
        self.mate = None
        self.sex = random.choice(SEXLIST)
        self.alive = True
        self.age = 0
        self.timebetweenmates = 0
        self.lookingForMate = False
        self.extraMovement = Queue()
        

        _map = self.CreateCreatureWorld()
        self.world = _map
    
    def RequestMate(self, mate):
        if self.mate == None:
            self.mate = mate
            return True
        else:return False


    def PotentialMateFound(self, mate):
        if mate.RequestMate(self):
            self.mate = mate
            return True
        else:return False

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

    
                       

    
        

    def FindPath(self,target):
        if target.position == self.position.position:print("error")
        self.world = self.CreateCreatureWorld() # i wanna remove THIS
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,target)
        pathfinder.InitiatePathfind()
        currentpath = pathfinder.path
        
        return currentpath
        

    def Wander(self,spawnableList):
        possibleWanderTiles = []
        for item in spawnableList:
            if self.GetDistanceBetween(self.position,item) <= MAXWANDERDISTANCE and item.position != self.position.position:
                possibleWanderTiles.append(item)

        cell = random.choice(possibleWanderTiles)
        cell = self.world[cell.position[0]][cell.position[1]]
        return cell


class Predator(Creature):
    def __init__(self,position,world,renderer,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,timebetweenmatespredator):
        super().__init__(position,world,renderer)
        self.BASE_ENERGY_PREDATOR = baseenergypredator
        self.MINDEATHAGE_PREDATOR = mindeathagepredator
        self.MAXDEATHAGE_PREDATOR = maxdeathagepredator
        self.ENERGYLOSSPERSTEP_PREDATOR = energylpredator
        self.TIMEBETWEENMATES_PREDATOR = timebetweenmatespredator
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"fox.png")).convert_alpha(),(self.CELLSIZE,self.CELLSIZE))
        self.preyTarget = None
        self.mateTarget = None
        self.energy = self.BASE_ENERGY_PREDATOR
        self.urgeReproduce = URGE_REPRODUCE_PREDATOR
        self.deathage = random.randint(self.MINDEATHAGE_PREDATOR,self.MAXDEATHAGE_PREDATOR)

    def LocateMate(self,lookingForMate):
        self.energy -= self.ENERGYLOSSPERSTEP_PREDATOR
        if self not in lookingForMate:
            lookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for creature in lookingForMate:
            if self.GetDistanceBetween(self.position,creature.position) < lowest and creature.sex != self.sex:
                closestmate = creature

        if closestmate != None:
            if self.mate == None:
                if self.sex == "f":
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m":
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            target = self.mate.position
                            self.mateTarget = target
                            if target.position != self.position.position:
                                self.currentpath = self.FindPath(target)



    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        if len(self.extraMovement.list) != 0 and len(self.currentpath.stack) == 0:
            self.position = self.extraMovement.RemoveFromQueue()
        else:
            self.position = self.currentpath.stack[self.currentpath.size]
            self.currentpath.RemoveFromStack()
        if self.preyTarget and self.preyTarget.position.position == self.position.position:
            self.energy = self.BASE_ENERGY_PREDATOR
            self.preyTarget.hasPredator = False
            self.preyTarget.predator = None
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            return 2

        


        if self.mate and self.mate.position.position == self.position.position:
            self.mateTarget = None
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE_PREDATOR
            self.mate.urgeReproduce = URGE_REPRODUCE_PREDATOR
            self.mate.mate = None
            self.mate = None
            return 1
        self.energy -= self.ENERGYLOSSPERSTEP_PREDATOR
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None



    def Hunt(self,preyList):
        lowest = 99999999
        lowestprey = None
        for prey in preyList:
            dist = self.GetDistanceBetween(prey.position,self.position)
            if not(prey.hasPredator) and dist < lowest:
                lowest = dist
                lowestprey = prey
        if lowestprey == None:
            return -1
        lowestprey.predator = self
        lowestprey.hasPredator = True
        self.preyTarget = lowestprey
        lowestpreyInCreatureWorld = self.world[lowestprey.position.position[0]][lowestprey.position.position[1]]
        return lowestpreyInCreatureWorld

    def Update(self,preyList,spawnableList,predatorLookingForMate):
        self.age += 1
        self.timebetweenmates += 1
        if self.age < MINREPROAGE_PREDATOR or self.timebetweenmates <= self.TIMEBETWEENMATES_PREDATOR:
            self.urgeReproduce -= URGELOSSPERSTEP
        if self.energy <= 0 or (self.age >= self.deathage):
            if self.mate:
                self.mate.mate = None
                self.mate = None
            if self.preyTarget:
                self.preyTarget.hasPredator = False
                self.preyTarget.predator = None
                self.preyTarget = None
                
            if self in predatorLookingForMate:
                predatorLookingForMate.remove(self)
            self.alive = False
            return -1
        if len(self.currentpath.stack) == 0 and len(self.extraMovement.list) == 0:
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            self.preyTarget = None
            option = self.ChooseActivity()
            match option[0]:
                case "f":
                    pass
                case "e":
                    target = self.Hunt(preyList)
                    if target == -1:
                        target = self.Wander(spawnableList)
                        self.currentpath = self.FindPath(target)
                    elif target.position == self.position.position:
                        self.currentpath.AddToStack(target)
                        self.AdvancePath()
                    else:
                        self.foodTarget = target
                        self.currentpath = self.FindPath(target)
                case "w":
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r":
                    self.LocateMate(predatorLookingForMate)
                        
        else:
            if self.mate:
                if self.mate.alive:
                    if self.preyTarget:
                        self.preyTarget.hasPredator = False
                        self.preyTarget.predator = None
                        self.preyTarget = None
                    if len(self.currentpath.stack) == 0 or (self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position):
                        target = self.mate.position
                        self.mateTarget = target
                        self.currentpath = self.FindPath(target)
                    elif self.sex[0] == "m" and self.mate.position.position != self.position.position:
                        action = self.AdvancePath()
                        if action == 1:
                            return 0
                    elif self.sex[0] == "m" and self.mate.position.position == self.position.position:
                        return 0

                else:
                    self.mate.mate = None
                    self.mate = None
                pass
            else:
                if self.preyTarget == None or self.preyTarget.alive:
                    action = self.AdvancePath()
                    if action == 2:
                        preyList.remove(self.preyTarget)
                        self.preyTarget.alive = False
                        self.preyTarget = None
                        pass
                    if self.preyTarget:
                        if self.preyTarget.position.position != self.foodTarget.position and self.extraMovement.BackOfQueue() != self.preyTarget.position:
                            self.extraMovement.AddToQueue(self.preyTarget.position)
                            pass
                else:
                    self.extraMovement.ClearQueue()
                    self.preyTarget.hasPredator = False
                    self.preyTarget.predator = None
                    self.preyTarget = None
                    self.currentpath.ClearStack()
                    
        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS.copy()

        choiceweights[0] += (self.BASE_ENERGY_PREDATOR-self.energy) #eat chance
        choiceweights[1] += (self.energy/self.BASE_ENERGY_PREDATOR + self.urgeReproduce/URGE_REPRODUCE_PREDATOR)*10 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE_PREDATOR-self.urgeReproduce)*MULTI  #chance to reproduce
        
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        if self.age < MINREPROAGE_PREDATOR or self.timebetweenmates <= self.TIMEBETWEENMATES_PREDATOR:
            choiceweights[2] = 0
        return random.choices(["e","w","r"],choiceweights,k=1)

class Prey(Creature):
    def __init__(self,position,world,renderer,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,timebetweenmatesprey):
        super().__init__(position,world,renderer)
        self.TIMEBETWEENMATES_PREY = timebetweenmatesprey
        self.BASE_ENERGY_PREY = baseenergyprey
        self.MINDEATHAGE_PREY = mindeathageprey
        self.MAXDEATHAGE_PREY = maxdeathageprey
        self.ENERGYLOSSPERSTEP_PREY = energylprey
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"rabbit.png")).convert_alpha(),(self.CELLSIZE,self.CELLSIZE))
        self.hasPredator = False
        self.energy = self.BASE_ENERGY_PREY
        self.predator = None
        self.urgeReproduce = URGE_REPRODUCE_PREY
        self.deathage = random.randint(self.MINDEATHAGE_PREY,self.MAXDEATHAGE_PREY)
    
    def LocateMate(self,lookingForMate):
        self.energy -= self.ENERGYLOSSPERSTEP_PREY
        if self not in lookingForMate:
            lookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for creature in lookingForMate:
            if self.GetDistanceBetween(self.position,creature.position) < lowest and creature.sex != self.sex:
                closestmate = creature

        if closestmate != None:
            if self.mate == None:
                if self.sex == "f":
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m":
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            target = self.mate.position
                            self.mateTarget = target
                            if target.position != self.position.position:
                                self.currentpath = self.FindPath(target)
  

    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        self.position = self.currentpath.stack[self.currentpath.size]
        self.currentpath.RemoveFromStack()
    
        if self.foodTarget and self.foodTarget.position == self.position.position:
            self.energy = self.BASE_ENERGY_PREY
            self.foodTarget.hasTarget = False
            return 0

        


        if self.mate and self.mate.position.position == self.position.position:
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE_PREY
            self.mate.urgeReproduce = URGE_REPRODUCE_PREY
            self.mate.mate = None
            self.mate = None
            return 1
        self.energy -= self.ENERGYLOSSPERSTEP_PREY
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        

    def Update(self,berryList,fertileList,spawnableList,preyLookingForMate):
        self.age += 1
        self.timebetweenmates += 1
        if self.age < MINREPROAGE_PREY or self.timebetweenmates <= self.TIMEBETWEENMATES_PREY:
            self.urgeReproduce -= URGELOSSPERSTEP
        if self.energy <= 0 or (self.age >= self.deathage):
            if self.mate:
                self.mate.mate = None
                self.mate = None
            if self.foodTarget:
                self.foodTarget.hasTarget = False
                self.foodTarget = None
                
            if self in preyLookingForMate:
                preyLookingForMate.remove(self)
            self.alive = False
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
                    elif target.position == self.position.position:
                        self.currentpath.AddToStack(target)
                        self.AdvancePath()
                    else:
                        self.currentpath = self.FindPath(target)
                case "w":
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r":
                    self.LocateMate(preyLookingForMate)
                        
        else:
            if self.mate:
                if self.mate.alive:
                    if self.foodTarget:
                        self.foodTarget.hasTarget = False
                        self.foodTarget.target = None
                        self.foodTarget = None
                    if self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position:
                        target = self.mate.position
                        self.currentpath = self.FindPath(target)
                    elif self.sex[0] == "m" and self.mate.position.position != self.position.position:
                        action = self.AdvancePath()
                        if action == 1:
                            return 0
                    elif self.sex[0] == "m" and self.mate.position.position == self.position.position:
                        return 0
                else:
                    self.mate.mate = None
                    self.mate = None

                pass
            else:
                action = self.AdvancePath()
                if action == 0:
                    berryList.remove(self.foodTarget)
                    fertileList.append(self.foodTarget)
                
                    

        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS.copy()
        if self.hasPredator:
            #return "f"
            pass

        choiceweights[0] += (self.BASE_ENERGY_PREY-self.energy) #eat chance
        choiceweights[1] += (self.energy/self.BASE_ENERGY_PREY + self.urgeReproduce/URGE_REPRODUCE_PREY)*10 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE_PREY-self.urgeReproduce)*MULTI  #chance to reproduce
        
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        if self.age < MINREPROAGE_PREY or self.timebetweenmates <= self.TIMEBETWEENMATES_PREY:
            choiceweights[2] = 0
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
        lowestberry.target = self
        lowestberry.hasTarget = True
        self.foodTarget = lowestberry
        lowestberryInCreatureWorld = self.world[lowestberry.position[0]][lowestberry.position[1]]
        return lowestberryInCreatureWorld

    def Flee(self):
        #run from the predator chasing
        pass


         


