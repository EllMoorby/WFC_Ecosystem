from constants import *
from pathfinder import PathFinder,Stack
import random
import math
import pygame

class Queue: #Create a queue class #####GROUP A - Queue ########
    def __init__(self):
        self.fPointer = 0 #Create a front pointer pointing to the first element of the queue
        self.rPointer = -1 #Create a back pointer pointing to the last element of the queue
        self.list = [] #The queue itself

    def AddToQueue(self,item): #Append an item at the end of the queue and increase the rear pointer
        self.rPointer += 1
        self.list.append(item)

    def RemoveFromQueue(self): #Pop the front item of the queue and return the item
        if self.fPointer <= self.rPointer:
            item = self.list[self.fPointer]
            self.list.pop(self.fPointer)
            self.rPointer-=1
            return item

    def ClearQueue(self): #Empty the queue and reset it
        self.fPointer = 0
        self.rPointer = -1
        self.list = []

    def BackOfQueue(self): #Returns the item in the back of a queue, unless it is empty then it returns nothing
        if self.fPointer <= self.rPointer:
            return self.list[self.rPointer]
        return
    


class CreatureCell:
    def __init__(self,position,tile) -> None:
        self.position = (position[0],position[1])
        self.tile = tile #The tile's tile object
        self.g_cost = 0 #dist of a cell from start
        self.h_cost = 0 #dist of a cell from end
        self.f_cost = 0 #Gcost+Hcost
        self.pointer = None #Pointer
        self.traversable = self.tile.traversable #Boolean, if the tile is traversable

class Creature: #Create a generic creature class #####GROUP A - OOP ########
    def __init__(self,position,world,renderer,cellsize,screenwidth,screenheight):
        self.CELLSIZE = cellsize
        self.SCREENWIDTH = screenwidth
        self.SCREENHEIGHT = screenheight
        self.position = position
        self.worldmap = world #The map of the current world
        self.currentpath = Stack() #Create a stack of the current path
        self.renderer = renderer #Create a renderer
        self.foodTarget = None #The food that the creature is targetting
        self.mate = None #The creatures current mate
        self.sex = random.choice(SEXLIST) #A random sex is chosen
        self.alive = True #Boolean of the creature is alive
        self.age = 0 #The current age of the creature in frames
        self.timebetweenmates = 0 #The time between mates in frames
        self.lookingForMate = False #Whether the creature is currently looking for a mate
        self.extraMovement = Queue() #Create a queu of extraMovement
        

        _map = self.CreateCreatureWorld() #The current map in creature cells
        self.world = _map


    def ChooseActivity(self): #Choose an activity #####GROUP A - OOP Polymorphism ########
        choiceweights = BASECHOICEWEIGHTS.copy()
        return random.choice(["e","w","r"]) #Make a random choice baced on weights
    
    def RequestMate(self, mate): #Accept the request to be a mate if the creature does not have a mate
        if self.mate == None:
            self.mate = mate
            return True
        else:return False


    def PotentialMateFound(self, mate): #Send a request to a potential mate to check if both are in need of a mate
        if mate.RequestMate(self):
            self.mate = mate
            return True
        else:return False

    def GetDistanceBetween(self,item1,item2): #return the distance between two cells, item1 and item2
        dx = item1.position[0] - item2.position[0]
        dy = item1.position[1] - item2.position[1]
        return math.sqrt(dx*dx + dy*dy)


    def CreateCreatureWorld(self): #Create a 2D array of creature cells, mirroring the world map
        world = []
        for index,row in enumerate(self.worldmap):
            world.append([])
            for cell in row:
                world[index].append(CreatureCell(cell.position,cell.tile))

        return world

    
                       

    
        

    def FindPath(self,target):
        if target.position == self.position.position:print("error")
        self.world = self.CreateCreatureWorld() #Create a 2D array of creature cells, mirroring the world map with cell costs
        pathfinder = PathFinder(self,target,self.SCREENHEIGHT,self.SCREENWIDTH,self.CELLSIZE) #Create a new pathfinder object to search the map
        pathfinder.InitiatePathfind() #Path find towards a target
        currentpath = pathfinder.path #Set the path the pathfinder found to the current path
        
        return currentpath
        

    def Wander(self,spawnableList): #Choose a random cell within a distance and pathfind there
        possibleWanderTiles = [] #List of all possible tiles within a range
        for item in spawnableList: #find all tiles which are spawnable
            if self.GetDistanceBetween(self.position,item) <= MAXWANDERDISTANCE and item.position != self.position.position:
                possibleWanderTiles.append(item)

        cell = random.choice(possibleWanderTiles) #Choose a random cell
        cell = self.world[cell.position[0]][cell.position[1]] #Transfer that cell to inworld positions
        return cell


class Predator(Creature): #Create the predator class, which inherits from the Creature class #####GROUP A - OOP Inheritance ########
    def __init__(self,position,world,renderer,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,timebetweenmatespredator,cellsize,screenwidth,screenheight,parentalGene=None):
        super().__init__(position,world,renderer,cellsize,screenwidth,screenheight)
        #Set all values imported from the eventManager to constants
        self.BASE_ENERGY_PREDATOR = baseenergypredator
        self.MINDEATHAGE_PREDATOR = mindeathagepredator
        self.MAXDEATHAGE_PREDATOR = maxdeathagepredator
        self.ENERGYLOSSPERSTEP_PREDATOR = energylpredator
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"fox.png")).convert_alpha(),(self.CELLSIZE,self.CELLSIZE)) #The scaled image of the predator
        self.preyTarget = None
        self.mateTarget = None
        self.energy = self.BASE_ENERGY_PREDATOR
        self.urgeReproduce = URGE_REPRODUCE_PREDATOR
        self.deathage = random.randint(self.MINDEATHAGE_PREDATOR,self.MAXDEATHAGE_PREDATOR) #A random deathage is chosen between two values
        if parentalGene == None: #If their parent has no parental gene, then they get a random gene strength
            self.gestationGene = random.randint(1,100)
        else: #If the parent has a parental gene, then it is changed slightly to advance mutation
            self.gestationGene = parentalGene + random.randint(-10,10)
            if self.gestationGene >= 100: #lock the value to 0 < gene < 100
                self.gestationGene = 100
            elif self.gestationGene < 0:
                self.gestationGene = 0
        
        self.MINREPROAGE = (MINREPROAGE_PREDATOR - MINREPROAGERANGE/2) + (MINREPROAGERANGE*(self.gestationGene/100)) #The minimum age a predator can reproduce is within a range which is determined by the strength of the gene
        self.TIMEBETWEENMATES_PREDATOR = (timebetweenmatespredator-TIMEBETWEENMATESRANGE/2) + (TIMEBETWEENMATESRANGE*(self.gestationGene/100)) #The time between predators reproducing is within a range which is determined by the strength of the gene

    def LocateMate(self,lookingForMate): #The locating of another mate
        self.energy -= self.ENERGYLOSSPERSTEP_PREDATOR # Lose energy per search
        if self not in lookingForMate: #Add self to the waiting list if not already
            lookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for creature in lookingForMate: #Search through all mates within the mating list and find the closest of the opposite gender
            dist = self.GetDistanceBetween(self.position,creature.position)
            if dist < lowest and creature.sex != self.sex:
                closestmate = creature
                lowest = dist

        if closestmate != None: #If the closest mate has been found
            if self.mate == None:
                if self.sex == "f":
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate): #If the request to be mate has been allowed remove both the predator and mate from the waiting list
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m":
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate): #If the request to be mate has been allowed remove both the predator and mate from the waiting list
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            #If the predator is male, start pathfinding towards female
                            target = self.mate.position
                            self.mateTarget = target
                            if target.position != self.position.position:
                                self.currentpath = self.FindPath(target)


    def AdvancePath(self): #Advance 1 cell forward across the map
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        if len(self.extraMovement.list) != 0 and len(self.currentpath.stack) == 0: #If no extra movement, and the path is empty, set position to the finish #####GROUP A - Stack/Queue Operations ########
            self.position = self.extraMovement.RemoveFromQueue()
        else: #Advance path by 1 and remove that from queue
            self.position = self.currentpath.stack[self.currentpath.size] #####GROUP A - Stack/Queue Operations ########
            self.currentpath.RemoveFromStack() 
        if self.preyTarget and self.preyTarget.position.position == self.position.position: #If they have reached their target, consume it
            self.energy = self.BASE_ENERGY_PREDATOR
            self.preyTarget.hasPredator = False
            self.preyTarget.predator = None
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            return 2 #Return code for consumed target

        


        if self.mate and self.mate.position.position == self.position.position: #If on current mate
            self.mateTarget = None
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE_PREDATOR
            self.mate.urgeReproduce = URGE_REPRODUCE_PREDATOR
            self.mate.mate = None
            self.mate = None
            return 1 #Return code for reproduce
        self.energy -= self.ENERGYLOSSPERSTEP_PREDATOR
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None



    def Hunt(self,preyList): #Choose the closest prey out of the list of prey
        lowest = 99999999
        lowestprey = None
        for prey in preyList: #Cycle through all the prey
            dist = self.GetDistanceBetween(prey.position,self.position)
            if not(prey.hasPredator) and dist < lowest: #If the prey is the closest so far and does not have a predator already
                lowest = dist
                lowestprey = prey
        if lowestprey == None: #If there are no huntable prey
            return -1
        lowestprey.predator = self
        lowestprey.hasPredator = True
        self.preyTarget = lowestprey
        lowestpreyInCreatureWorld = self.world[lowestprey.position.position[0]][lowestprey.position.position[1]] #Transfer the cell to inworld positions
        return lowestpreyInCreatureWorld

    def Update(self,preyList,spawnableList,predatorLookingForMate,predatorList): #Main update loop
        self.age += 1 #Add one to age every frame
        self.timebetweenmates += 1 
        if self.age < MINREPROAGE_PREDATOR or self.timebetweenmates <= self.TIMEBETWEENMATES_PREDATOR: #If the the predator is old enough to mate and had enough time between previous mates
            self.urgeReproduce -= URGELOSSPERSTEP #Start becoming more needing to reproduce
        if self.energy <= 0 or (self.age >= self.deathage): #If the predator has died from either old age or energy loss
            if self.mate: #Clear the mates
                self.mate.mate = None
                self.mate = None
            if self.preyTarget: #Clear the targets
                self.preyTarget.hasPredator = False
                self.preyTarget.predator = None
                self.preyTarget = None
                
            if self in predatorLookingForMate: #Remove self from mating list
                predatorLookingForMate.remove(self)
            self.alive = False
            return -1
        if len(self.currentpath.stack) == 0 and len(self.extraMovement.list) == 0: #If no movement to go
            self.foodTarget = None
            self.extraMovement.ClearQueue()
            self.preyTarget = None
            option = self.ChooseActivity() #Choose an activity
            match option[0]:
                case "e": #Eat has been chosen
                    target = self.Hunt(preyList) #Choose a target
                    if target == -1: #If target has not been found
                        target = self.Wander(spawnableList) #Find random spawnable cell around predator
                        self.currentpath = self.FindPath(target) #Pathfind to random target
                    elif target.position == self.position.position: #If the predator is on the target, then stay and eat the target
                        self.currentpath.AddToStack(target)
                        self.AdvancePath()
                    else: #Otherwise pathfind to the target
                        self.foodTarget = target
                        self.currentpath = self.FindPath(target)
                case "w": #Wander to a location
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r": #Locate a mate
                    self.LocateMate(predatorLookingForMate)
                        
        else:
            if self.mate: #If they have a mate
                if self.mate.alive or self.mate not in predatorList: #If the mate has died
                    if self.preyTarget: #Clear targets
                        self.preyTarget.hasPredator = False
                        self.preyTarget.predator = None
                        self.preyTarget = None
                    if len(self.currentpath.stack) == 0 or (self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position): #If the stack is empty, start filling the queue
                        target = self.mate.position
                        self.mateTarget = target
                        self.currentpath = self.FindPath(target)
                    elif self.sex[0] == "m" and self.mate.position.position != self.position.position: #If male, move towards target
                        action = self.AdvancePath() 
                        if action == 1:
                            return 0
                    elif self.sex[0] == "m" and self.mate.position.position == self.position.position: #If female, stand still
                        return 0

                else:
                    self.mate.mate = None
                    self.mate = None
                pass
            else:
                if self.preyTarget == None or self.preyTarget.alive: #If the predator has a target which is alive, or has no target, follow the path
                    action = self.AdvancePath()
                    if action == 2: #Remove prey target if the predato has reached them
                        preyList.remove(self.preyTarget)
                        self.preyTarget.alive = False
                        self.preyTarget = None
                        pass
                    if self.preyTarget: #Add extra movement after the stack is empty
                        if self.preyTarget.position.position != self.foodTarget.position and self.extraMovement.BackOfQueue() != self.preyTarget.position:
                            self.extraMovement.AddToQueue(self.preyTarget.position)
                            pass
                else: #Otherwise clear all
                    self.extraMovement.ClearQueue()
                    self.preyTarget.hasPredator = False
                    self.preyTarget.predator = None
                    self.preyTarget = None
                    self.currentpath.ClearStack()
                    
        self.renderer.DrawCreature(self) #Draw creature

    def ChooseActivity(self): #Choose an activity #####GROUP A - OOP Polymorphism ########
        choiceweights = BASECHOICEWEIGHTS.copy()

        choiceweights[0] += (100-((self.energy/self.BASE_ENERGY_PREDATOR)*100))+random.randint(-URGETOEATRANGE,URGETOEATRANGE) #Chance to eat
        choiceweights[1] += (((self.energy/self.BASE_ENERGY_PREDATOR)*100)+((self.urgeReproduce/URGE_REPRODUCE_PREDATOR)*100))/2 #Chance to wander
        choiceweights[2] += 100-((self.urgeReproduce/URGE_REPRODUCE_PREDATOR)*100)  #Chance to reproduce
        
        for index,weight in enumerate(choiceweights): #For each weight
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT) #Ensure the weight is between MAXCHOICEWEIGHT and 0.1
            choiceweights[index] = weight
        if self.age < MINREPROAGE_PREDATOR or self.timebetweenmates <= self.TIMEBETWEENMATES_PREDATOR: #If the predator is too young or too close between mates, the urge to reproduce is set to 0
            choiceweights[2] = 0


        if choiceweights[1] == max(choiceweights): #If wander is the maxiumum, always wander
            return ["w"]
        else:
            return random.choices(["e","w","r"],choiceweights,k=1) #Make a random choice baced on weights

class Prey(Creature):
    def __init__(self,position,world,renderer,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,timebetweenmatesprey,cellsize,screenwidth,screenheight,parentGestationGene=None):
        super().__init__(position,world,renderer,cellsize,screenwidth,screenheight)
        #Set all base variable for the prey
        self.BASE_ENERGY_PREY = baseenergyprey
        self.MINDEATHAGE_PREY = mindeathageprey
        self.MAXDEATHAGE_PREY = maxdeathageprey
        self.ENERGYLOSSPERSTEP_PREY = energylprey
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"rabbit.png")).convert_alpha(),(self.CELLSIZE,self.CELLSIZE)) #Set and scale prey image
        self.hasPredator = False
        self.energy = self.BASE_ENERGY_PREY
        self.predator = None
        self.urgeReproduce = URGE_REPRODUCE_PREY
        self.deathage = random.randint(self.MINDEATHAGE_PREY,self.MAXDEATHAGE_PREY) #Choose a random death age for the prey
        if parentGestationGene == None: #If the parent has no gene, create a randomn gene
            self.gestationGene = random.randint(1,100)
        else:
            self.gestationGene = parentGestationGene + random.randint(-10,10) #Random mutation from parents gene
            #Ensure the gene is between 100 and 0 
            if self.gestationGene >= 100:
                self.gestationGene = 100
            elif self.gestationGene < 0:
                self.gestationGene = 0
        self.numberOfOffspring = math.ceil((MAXOFFSPRING_PREY * (self.gestationGene/100))) #Number of offspring based off of the gestation gene
        self.MINREPROAGE = (MINREPROAGE_PREY - MINREPROAGERANGE/2) + (MINREPROAGERANGE*(self.gestationGene/100)) #Minimum reproduction age based off gestation gene
        self.TIMEBETWEENMATES_PREY = (timebetweenmatesprey-TIMEBETWEENMATESRANGE/2) + (TIMEBETWEENMATESRANGE*(self.gestationGene/100)) #Time between mates based off gestation gene
    
    def LocateMate(self,lookingForMate): #Find a mate #####GROUP B - Simple user defined algorithms ########
        self.energy -= self.ENERGYLOSSPERSTEP_PREY #Lose energy every time they mate
        if self not in lookingForMate: #Add self to mating list, if not in the list already
            lookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for creature in lookingForMate: #Cycle through all others looking for mate #####GROUP C - Linear Search ########
            dist = self.GetDistanceBetween(self.position,creature.position)
            if dist < lowest and creature.sex != self.sex: #Find the closest mate of opposite sex so far
                closestmate = creature
                lowest = dist

        if closestmate != None: #If there is a mate
            if self.mate == None:
                if self.sex == "f": #Request mate
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m": #Request mate
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate):
                            lookingForMate.remove(self)
                            lookingForMate.remove(self.mate)
                            target = self.mate.position
                            self.mateTarget = target
                            if target.position != self.position.position: #If male and not on they mate, pathfind to target
                                self.currentpath = self.FindPath(target)
  

    def AdvancePath(self): #Advance along a current path
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        self.position = self.currentpath.stack[self.currentpath.size] #Set current position to the item on the top of the stack
        self.currentpath.RemoveFromStack() #Remove the last item from the top of the stack
    
        if self.foodTarget and self.foodTarget.position == self.position.position: #If there is a food target and the prey is in that location, consume the target
            self.energy = self.BASE_ENERGY_PREY
            self.foodTarget.hasTarget = False
            return 0 #Return the code for consume target

        


        if self.mate and self.mate.position.position == self.position.position: #If have a mate and on the same location, mate
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE_PREY
            self.mate.urgeReproduce = URGE_REPRODUCE_PREY
            self.mate.mate = None
            self.mate = None
            return 1 #Return code for reproduce
        self.energy -= self.ENERGYLOSSPERSTEP_PREY #Lose energy per step moved
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        

    def Update(self,berryList,fertileList,spawnableList,preyLookingForMate): #Main update loop
        self.age += 1 #Increase age once per frame
        self.timebetweenmates += 1
        if self.age < self.MINREPROAGE or self.timebetweenmates <= self.TIMEBETWEENMATES_PREY: #If the prey is older than min age to reproduce and have had sufficient time between mates, they should have urge to reproduce
            self.urgeReproduce -= URGELOSSPERSTEP
        if self.energy <= 0 or (self.age >= self.deathage): #Check if the prey has died of old age or energy loss
            if self.mate: #Clear the mates
                self.mate.mate = None
                self.mate = None
            if self.foodTarget: #Clear the targets
                self.foodTarget.hasTarget = False
                self.foodTarget = None
                
            if self in preyLookingForMate: #Remove self from mating list
                preyLookingForMate.remove(self)
            self.alive = False
            return -1
        if len(self.currentpath.stack) == 0: #If the path is empty
            self.foodTarget = None
            option = self.ChooseActivity() #Choose an activity
            match option[0]:
                case "e": #Pathfind to the closest berry
                    target = self.Forage(berryList) #Attempt to find food
                    if target == -1: #If there is no food, wander around instead
                        target = self.Wander(spawnableList)
                        self.currentpath = self.FindPath(target)
                    elif target.position == self.position.position: #If the prey is on the same position as the target, stay still
                        self.currentpath.AddToStack(target)
                        self.AdvancePath()
                    else:
                        self.currentpath = self.FindPath(target) #Otherwise pathfind towards target
                case "w": #Wander to a spawnable location within a range
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r": #Locate a mate and reproduce
                    self.LocateMate(preyLookingForMate)
                        
        else:
            if self.mate: 
                if self.mate.alive: #If the prey has an alive mate
                    if self.foodTarget: #Stop searching for food
                        self.foodTarget.hasTarget = False
                        self.foodTarget.target = None
                        self.foodTarget = None
                    if self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position: #If the prey with mate is not targetting the mate, change target to mate
                        target = self.mate.position
                        self.currentpath = self.FindPath(target) #Pathfind to the target
                    elif self.sex[0] == "m" and self.mate.position.position != self.position.position: #If the prey is male and has not reached it's mate, advance the path
                        action = self.AdvancePath()
                        if action == 1: #If target has been reached, return 0
                            return 0 #Return code for reproduce
                    elif self.sex[0] == "m" and self.mate.position.position == self.position.position: #If destination has been reached, return 0
                        return 0 #Return code for reproduce
                else: #Clear mates
                    self.mate.mate = None
                    self.mate = None

                pass
            else:
                action = self.AdvancePath() #Advance path
                if action == 0: #If code for food has been eaten
                    berryList.remove(self.foodTarget)
                    fertileList.append(self.foodTarget)
                
                    

        self.renderer.DrawCreature(self) #Render creature

    def ChooseActivity(self): #Choose an activity
        choiceweights = BASECHOICEWEIGHTS.copy()

        choiceweights[0] += (self.BASE_ENERGY_PREY-self.energy) #Chance to eat
        choiceweights[1] += (self.energy/self.BASE_ENERGY_PREY + self.urgeReproduce/URGE_REPRODUCE_PREY)*10 #Chance to wander
        choiceweights[2] += (URGE_REPRODUCE_PREY-self.urgeReproduce)*MULTI  #Chance to reproduce
        
        for index,weight in enumerate(choiceweights): #For weight in list
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT) #Ensure that the weight is within the allowed range
            choiceweights[index] = weight
        if self.age < self.MINREPROAGE or self.timebetweenmates <= self.TIMEBETWEENMATES_PREY: #If the prey is too young or mated too recently, have no urge to reproduce
            choiceweights[2] = 0
        return random.choices(["e","w","r"],choiceweights,k=1) #Return a random choice based off of the weights set

    def Forage(self,berryList): #Locate the nearest berry
        lowest = 99999999
        lowestberry = None
        for berry in berryList: #Cycle through all berrys
            dist = self.GetDistanceBetween(berry,self.position)
            if not(berry.hasTarget) and dist < lowest: #Find the closest berry which is untargetted
                lowest = dist
                lowestberry = berry
        if lowestberry == None: #If there is no berrys available, return -1
            return -1
        lowestberry.target = self
        lowestberry.hasTarget = True
        self.foodTarget = lowestberry
        lowestberryInCreatureWorld = self.world[lowestberry.position[0]][lowestberry.position[1]] #Transfer berry location to inworld position
        return lowestberryInCreatureWorld