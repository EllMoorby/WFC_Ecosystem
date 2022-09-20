from random import choice
from constants import *
from ecosystem import Predator,PredatorFemale,Prey,PreyFemale
from renderer import Renderer
from engine import Engine
import pygame
from waveFunctionCollapse import GenerateMap

class EventManager:
    def __init__(self):
        self.creaturecount = CREATURECOUNT
        self.world = []
        self.berryList = []
        self.preyList = []
        self.predatorList = []
        self.renderer = Renderer()    
        self.engine = Engine()
        self.tilelist = []
        self.tiledict = {}
        self.fertileList = []
        self.spawnableList = []

    def SplitWorld(self):
        self.tiledict = {}
        self.berryList = []
        self.fertileList = []
        for tile in self.tilelist:
            self.tiledict[tile] = []

        for row in self.world:
            for cell in row:
                for key in self.tiledict:
                    if cell.tile == key:
                        self.tiledict[key].append(cell)


        for key in self.tiledict:
            if key.fertile:
                for item in self.tiledict[key]:
                    self.fertileList.append(item)

            if key.traversable:
                for item in self.tiledict[key]:
                    self.spawnableList.append(item)
                


    def CreateWorld(self):
        while True:
            world,self.tilelist = GenerateMap()
            try:
                pass
                #self.renderer.RenderWorld(self.world)
            except:
                continue
            else:
                return world


    def SpawnBerry(self):
        newberry = choice(self.fertileList)
        self.berryList.append(newberry)
        self.fertileList.remove(newberry)
        self.renderer.RenderBerry(newberry)
        pass

    def InitializeCreatures(self):
        for creature in range(self.creaturecount):
            self.preyList.append(Prey(choice(self.spawnableList).position,"img",self.world,self.renderer))
        pass

    def Update(self):
        for creature in self.preyList:
            creature.Update()
            print(self.preyList)
            print("update")
        
        pass

    def Main(self):
        self.world = self.CreateWorld()
        self.SplitWorld()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.world = self.CreateWorld()
                        self.SplitWorld()
                    if event.key == pygame.K_o:
                        self.Update()
                    if event.key == pygame.K_u:
                        self.SpawnBerry()
                    if event.key == pygame.K_w:
                        self.InitializeCreatures()
                if event.type == pygame.QUIT:
                    playing = False