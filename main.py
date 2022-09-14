import pygame
from waveFunctionCollapse import *
from constants import *
from engine import Engine
from renderer import Renderer
from ecosystem import Prey
from pathfinder import PathFinder
import sys

sys.setrecursionlimit(6**10)



engine = Engine() 
renderer = Renderer()



def CreateWorld():
    while True:
        world = GenerateMap()
        try:
            renderer.RenderWorld(world)
        except:
            continue
        else:
            return world

world = CreateWorld()
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                world = CreateWorld()
                prey = Prey((0,0),"test",world)
            if event.key == pygame.K_o:

                prey.Move("tere", renderer,world)


