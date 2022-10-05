from distutils.command.clean import clean
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
            print("pointer",self.fPointer)
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
            print("self.rPointer",self.rPointer)
            print("self.fPointer",self.fPointer)
            print(self.list)
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
        self.sex = random.choice(SEXLIST)
        self.alive = True
        self.age = 0
        self.deathage = random.randint(MINDEATHAGE,MAXDEATHAGE)
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

    def LocateMate(self,preyLookingForMate):
        self.energy -= LOSSPERSTEP
        if self not in preyLookingForMate:
            preyLookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for prey in preyLookingForMate:
            if self.GetDistanceBetween(self.position,prey.position) < lowest and prey.sex != self.sex:
                closestmate = prey

        if closestmate != None:
            if self.mate == None:
                if self.sex == "f":
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate):
                            preyLookingForMate.remove(self)
                            preyLookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m":
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate):
                            preyLookingForMate.remove(self)
                            preyLookingForMate.remove(self.mate)
                            target = self.mate.position
                            if target.position != self.position.position:
                                self.currentpath = self.FindPath(target)
                       

    
        

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
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"fox.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.urgeHunt = URGE_HUNT
        self.preyTarget = None
        self.foodTarget = None



    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        if len(self.extraMovement.list) != 0 and len(self.currentpath.stack) == 0:
            self.position = self.extraMovement.RemoveFromQueue()
            print("remov")
            print("updated movelist",self.extraMovement.list)
        else:
            self.position = self.currentpath.stack[self.currentpath.size]
            self.currentpath.RemoveFromStack()
        print("preytarget",self.preyTarget)
        if self.preyTarget:
            print("their pos",self.preyTarget.position.position,"my pos", self.position.position)
        if self.preyTarget and self.preyTarget.position.position == self.position.position:
            print("here")
            self.energy = BASE_ENERGY
            self.preyTarget.hasPredator = False
            self.preyTarget.predator = None
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            return 2


        

        print("stack")    
        for item in self.currentpath.stack:
            print(item.position,end=" ")
        print(" ")
        print("extra movement",self.extraMovement.list)
        


        if self.mate and self.mate.position.position == self.position.position:
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE
            self.mate.urgeReproduce = URGE_REPRODUCE
            self.mate.mate = None
            self.mate = None
            return 1
        self.energy -= LOSSPERSTEP
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
        print(preyList)
        self.age += 1
        self.timebetweenmates += 1
        if self.age < MINREPROAGE_PREDATOR or self.timebetweenmates <= TIMEBETWEENMATES_PREDATOR:
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
        if len(self.currentpath.stack) == 0 and len(self.extraMovement.list) == 0 and not(self.preyTarget):
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            self.preyTarget = None
            option = self.ChooseActivity()
            match option[0]:
                case "f":
                    pass
                case "e":
                    print("eat")
                    target = self.Hunt(preyList)
                    print("target",target)
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
                if self.preyTarget:
                    self.preyTarget.hasPredator = False
                    self.preyTarget.predator = None
                    self.preyTarget = None
                if self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position:
                    target = self.mate.position
                    self.currentpath = self.FindPath(target)
                elif self.sex[0] == "m" and self.mate.position.position != self.position.position:
                    action = self.AdvancePath()
                    if action == 1:
                        return 0
                elif self.sex[0] == "m" and self.mate.position.position == self.position.position:
                    return 0

                pass
            else:
                action = self.AdvancePath()
                print("action",action)
                if action == 2:
                    print(preyList)
                    print(self.preyTarget)
                    preyList.remove(self.preyTarget)
                    self.preyTarget.alive = False
                    self.preyTarget = None
                    pass
                if self.preyTarget:
                    if self.preyTarget.position.position != self.foodTarget.position and self.extraMovement.BackOfQueue() != self.preyTarget.position:
                        self.extraMovement.AddToQueue(self.preyTarget.position)
                        pass
                    
        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS.copy()

        choiceweights[0] += (BASE_ENERGY-self.energy) #eat chance
        choiceweights[1] += (self.energy/BASE_ENERGY + self.urgeReproduce/URGE_REPRODUCE)*10 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE-self.urgeReproduce)*MULTI  #chance to reproduce
        
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        if self.age < MINREPROAGE or self.timebetweenmates <= TIMEBETWEENMATES:
            choiceweights[2] = 0
        return random.choices(["e","w","r"],choiceweights,k=1)

class Prey(Creature):
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"rabbit.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.hasPredator = False
        self.health = BASE_HEALTH
        self.predator = None
  

    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        self.position = self.currentpath.stack[self.currentpath.size]
        self.currentpath.RemoveFromStack()
    
        if self.foodTarget and self.foodTarget.position == self.position.position:
            self.energy = BASE_ENERGY
            self.foodTarget.hasTarget = False
            return 0

        


        if self.mate and self.mate.position.position == self.position.position:
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE
            self.mate.urgeReproduce = URGE_REPRODUCE
            self.mate.mate = None
            self.mate = None
            return 1
        self.energy -= LOSSPERSTEP
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        

    def Update(self,berryList,fertileList,spawnableList,preyLookingForMate):
        self.age += 1
        self.timebetweenmates += 1
        if self.age < MINREPROAGE or self.timebetweenmates <= TIMEBETWEENMATES:
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

                pass
            else:
                action = self.AdvancePath()
                print(action)
                if action == 0:
                    berryList.remove(self.foodTarget)
                    fertileList.append(self.foodTarget)
                
                    

        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS.copy()
        if self.hasPredator:
            #return "f"
            pass

        choiceweights[0] += (BASE_ENERGY-self.energy) #eat chance
        choiceweights[1] += (self.energy/BASE_ENERGY + self.urgeReproduce/URGE_REPRODUCE)*10 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE-self.urgeReproduce)*MULTI  #chance to reproduce
        
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        if self.age < MINREPROAGE or self.timebetweenmates <= TIMEBETWEENMATES:
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


         


