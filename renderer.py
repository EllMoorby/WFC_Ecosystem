import pygame
from constants import *

class Renderer: #Create a renderer class
    def __init__(self,screenwidth,screenheight,cellsize):
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.cellsize = cellsize
        self.screen = pygame.display.set_mode([screenwidth, screenheight]) #set the size of the screen to the screen dimensions
        self.screen.fill([0, 0, 0]) #Fill the screen with black to begin with
        self.berryimg = pygame.transform.scale(pygame.image.load(BERRYIMG).convert_alpha(),(self.cellsize,self.cellsize)) # Load the berry image to the correct scale
    

    def DrawCell(self,cell): #Draw cell at it's current position
        self.screen.blit(cell.tile.img,(cell.position[0]*self.cellsize,cell.position[1]*self.cellsize))
    
    def ClearScreen(self): #Fill the screen in with black
        self.screen.fill([0, 0, 0])

    def RenderWorld(self,world): #Draw every cell in the world
        for row in world:
            for cell in row:
                self.DrawCell(cell)


    def DrawCreature(self,creature): #Draw a creature at it's current cell position
        self.screen.blit(creature.img,(creature.position.position[0]*self.cellsize,creature.position.position[1]*self.cellsize))


    def RenderBerry(self,cell): #Draw a berry at it's current cell position
        self.screen.blit(self.berryimg,(cell.position[0]*self.cellsize,cell.position[1]*self.cellsize))

    def DrawText(self,text): #Display given text in the top left of the screen
        pygame.font.init()
        font = pygame.font.SysFont("Bahnschrift",20)
        text = font.render(text,True,(0,0,0))

        self.screen.blit(text,(0,0))
