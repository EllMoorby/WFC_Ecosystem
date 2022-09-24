from random import choice
from constants import *
from ecosystem import Predator,PredatorFemale,Prey,PreyFemale
from renderer import Renderer
from engine import Engine
import pygame
from waveFunctionCollapse import GenerateMap
import pstats

class EventManager:
    def __init__(self):
        self.creaturecount = CREATURECOUNT #Number of creatures
        self.world = [] #The current map
        self.berryList = [] #A list of all berrys
        self.preyList = [] #A list of prey instantiated
        self.predatorList = [] #A list of all predators instantiated
        self.renderer = Renderer() #Creature a new renderer, for renderering
        self.engine = Engine() #Create a new engine, for deltatime and FPS
        self.tilelist = [] #A list of all possible tiles
        self.tiledict = {} #Dictionary of all tile types
        self.fertileList = [] #A list of all fertile land where berrys can grow
        self.spawnableList = [] #A list of all tiles where creatures can spawn

    def SplitWorld(self): #split the world into fertile, spawnable land into a dictionary
        #reset all values, a new world was created
        self.tiledict = {}
        self.berryList = []
        self.fertileList = []
        self.spawnableList = []

        #expand the dictionary to allow all tiles to be added as keys
        for tile in self.tilelist:
            self.tiledict[tile] = []
        #tiles get added as keys
        for row in self.world:
            for cell in row:
                for key in self.tiledict:
                    if cell.tile == key:
                        self.tiledict[key].append(cell)

        #create list of fertile tiles and traversable from the dictionary
        for key in self.tiledict:
            if key.fertile:
                for item in self.tiledict[key]:
                    self.fertileList.append(item)

            if key.traversable:
                for item in self.tiledict[key]:
                    self.spawnableList.append(item)
                


    def CreateWorld(self): #create a world
        while True:
            #attempt to create a new world
            self.preyList = []
            self.predatorList = []
            world,self.tilelist = GenerateMap()
            pygame.display.flip()
            return world
            """try:
                pass
                #self.renderer.RenderWorld(self.world)
            except:
                continue
            else:
                return world"""


    def SpawnBerry(self): #spawn a berry at a random fertile spot
        newberry = choice(self.fertileList)
        newberry.hasBerry = True #ensure the tile knows it has a berry attatched
        self.berryList.append(newberry)
        self.fertileList.remove(newberry)
        self.renderer.RenderBerry(newberry) #render the berry
        pass

    def InitializeCreatures(self): #instantiate all creatures using the amount of creatures determined from constants
        
        for creature in range(self.creaturecount):
            #give them a random position, an image and pass both world + renderer as parameters
            self.preyList.append(Prey(choice(self.spawnableList),self.world,self.renderer))

    def Update(self): #update to be looped once per frame
        self.renderer.RenderWorld(self.world) #draw world
        #update all creatures
        for creature in self.preyList:
            creature.Update(self.berryList,self.fertileList,self.spawnableList)
        pygame.display.flip()
        

    def Main(self,pr): #main program
        self.world = self.CreateWorld() #generate a world
        self.SplitWorld() #split the world into fertile,spawnable,etc.
        self.InitializeCreatures()
        playing = True # create a playing loop
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.world = self.CreateWorld()
                        self.SplitWorld()
                        self.InitializeCreatures()
                    if event.key == pygame.K_u:
                        self.SpawnBerry()
                if event.type == pygame.QUIT:
                    stats = pstats.Stats(pr)
                    stats.sort_stats(pstats.SortKey.TIME)
                    stats.dump_stats(filename="test.prof")

                    playing = False

            self.Update()
            self.engine.update_dt()

                