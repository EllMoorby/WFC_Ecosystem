import pygame
from WaveFunctionCollapse import GetPossibleTiles
from constants import *
from engine import Engine
engine = Engine()

screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])

tiles = GetPossibleTiles()
for tile in tiles:
    print(tile.name)
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

