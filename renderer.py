import pygame
from constants import *

class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
        self.screen.fill([0, 0, 0])
        self.berryimg = pygame.transform.scale(pygame.image.load(BERRYIMG).convert_alpha(),(CELLSIZE,CELLSIZE))
    

    def DrawCell(self,cell):
        self.screen.blit(cell.tile.img,(cell.position[0]*CELLSIZE,cell.position[1]*CELLSIZE))
    
    def ClearScreen(self):
        self.screen.fill([0, 0, 0])

    def RenderWorld(self,world):
        for row in world:
            for cell in row:
                self.DrawCell(cell)


    def DrawCreature(self,creature):
        self.screen.blit(creature.img,(creature.position.position[0]*CELLSIZE,creature.position.position[1]*CELLSIZE))


    def RenderBerry(self,cell):
        self.screen.blit(self.berryimg,(cell.position[0]*CELLSIZE,cell.position[1]*CELLSIZE))
