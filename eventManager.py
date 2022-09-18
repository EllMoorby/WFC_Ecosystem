import imghdr
from random import choice
from unicodedata import name
from ecosystem import Predator,PredatorFemale,Prey,PreyFemale
from renderer import Renderer
from engine import Engine
import pygame
from waveFunctionCollapse import GenerateMap

class EventManager:
    def __init__(self):
        self.world = []
        self.berryList = []
        self.preyList = []
        self.predatorList = []
        self.renderer = Renderer()    
        self.engine = Engine()
        self.tilelist = []
        self.tiledict = {}
        self.fertileList = []

    def SplitWorld(self):
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
                


    def CreateWorld(self):
        while True:
            self.world,self.tilelist = GenerateMap()
            try:
                self.renderer.RenderWorld(self.world)
            except:
                continue
            else:
                return


    def SpawnBerry(self):
        newberry = choice(self.fertileList)
        self.berryList.append(newberry)
        self.renderer.RenderBerry(newberry)
        pass

    def InitializeCreatures():
        #spawn all the necessary creatures for the variables set
        pass

    def Update(self):
        #update all
        
        pass

    def Main(self):
        self.CreateWorld()
        self.SplitWorld()
        playing = True
        while playing:
            self.Update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.world = self.CreateWorld()
                        prey = Prey((0,0),"test",self.world)
                    if event.key == pygame.K_o:
                        prey.Move("tere", self.renderer,self.world.copy())
                    if event.key == pygame.K_i:
                        prey.AdvancePath(self.renderer)
                    if event.key == pygame.K_u:
                        self.SpawnBerry()
                if event.type == pygame.QUIT:
                    playing = False