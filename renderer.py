import pygame
from constants import *

class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
        self.screen.fill([0, 0, 0])
    

    def DrawCell(self,cell):
        self.screen.blit(cell.tile.img,(cell.position[0]*CELLSIZE,cell.position[1]*CELLSIZE))
        pygame.display.flip()
    
    def ClearScreen(self):
        self.screen.fill([0, 0, 0])

    def RenderWorld(self,world):
        for row in world:
            for cell in row:
                self.DrawCell(cell)

        pygame.display.flip()

    def DrawCreature(self,creature):
        self.screen.blit(creature.img,(creature.position[0]*CELLSIZE,creature.position[1]*CELLSIZE))
        pygame.display.flip()
