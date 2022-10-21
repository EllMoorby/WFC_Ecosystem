import pygame
from constants import *

class Renderer:
    def __init__(self,screenwidth,screenheight,cellsize):
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.cellsize = cellsize
        self.screen = pygame.display.set_mode([screenwidth, screenheight])
        self.screen.fill([0, 0, 0])
        self.berryimg = pygame.transform.scale(pygame.image.load(BERRYIMG).convert_alpha(),(self.cellsize,self.cellsize))
    

    def DrawCell(self,cell):
        self.screen.blit(cell.tile.img,(cell.position[0]*self.cellsize,cell.position[1]*self.cellsize))
    
    def ClearScreen(self):
        self.screen.fill([0, 0, 0])

    def RenderWorld(self,world):
        for row in world:
            for cell in row:
                self.DrawCell(cell)


    def DrawCreature(self,creature):
        self.screen.blit(creature.img,(creature.position.position[0]*self.cellsize,creature.position.position[1]*self.cellsize))


    def RenderBerry(self,cell):
        self.screen.blit(self.berryimg,(cell.position[0]*self.cellsize,cell.position[1]*self.cellsize))

    def DrawText(self,text):
        pygame.font.init()
        font = pygame.font.SysFont("Bahnschrift",20)
        text = font.render(text,True,(0,0,0))

        self.screen.blit(text,(0,0))
