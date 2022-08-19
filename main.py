import pygame
from WaveFunctionCollapse import *
from constants import *
from engine import Engine
engine = Engine()

screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])


GenerateMap()

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

