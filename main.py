import pygame
from WaveFunctionCollapse import *
from constants import *
from engine import Engine
from renderer import Renderer
import sys

sys.setrecursionlimit(3000)
engine = Engine()

#renderer = Renderer()

def CreateWorld():
    while True:
        world = GenerateMap()
        try:
            pass
            #renderer.RenderWorld(world)
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

