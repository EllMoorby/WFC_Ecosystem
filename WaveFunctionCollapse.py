from tracemalloc import start
from turtle import position
from constants import *
import json
import random


class Tile():
    def __init__(self,img,name) -> None:
        self.img = img #png of file
        self.adjacencylist = [] #List of other tiles allowed to TOUCH
        self.name = name

class Cell():
    def __init__(self,possibletiles,position) -> None:
        self.position = position
        self.possibletiles = possibletiles # list of possible tiles
        self.tile = None

class Chunk():
    def __init__(self,cells) -> None:
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)


def GetAdjacencyList(tilelist):
    #temporary
    #"adjacency":["grass","sand"]
    tilelist[0].adjacencylist = [tilelist[0],tilelist[2]]
    #"adjacency":["water","sand"]
    tilelist[1].adjacencylist = [tilelist[1],tilelist[2]]
    #"adjacency":["water","sand","grass"]
    tilelist[2].adjacencylist = [tilelist[0],tilelist[1],tilelist[2]]

def Collapse(origincell,newcell):
    originadjacencylist = origincell.tile.adjacencylist
    newpossibletiles = newcell.possibletiles
    print("possibletiles",newpossibletiles)
    print("origin adjacent",originadjacencylist)
    for item in newpossibletiles:
        print(item)
        if item not in originadjacencylist:
            newpossibletiles.remove(item)
    newcell.possibletiles = newpossibletiles
    print("after possibletiles",newpossibletiles)

def Propogate(cell,world):
    #check surrounding cells
    for x in range(-1,2):
        for y in range(-1,2):
            try:
                if x==y and x==0:
                    raise ValueError
                Collapse(cell,world[cell.position[0]+x][cell.position[1]+y]) #collapse items not in the tiles adjacencylist from the other cells possible tiles
            except:
                print("outta range")

    

def RandomTileFromPossible(cell):
    return random.choice(cell.possibletiles)
    
def GetPossibleTiles():
    tilelist = []
    with open(path.join(TILES_FOLDER,"textures.json")) as f:
        data = json.load(f)
        for tile in data["tiles"]:
            tilelist.append(Tile(tile["image"],tile["name"]))

    return tilelist

def GenerateMap():
    possibletiles = GetPossibleTiles()
    GetAdjacencyList(possibletiles)
    world = []
    for celly in range(SCREENHEIGHT // CELLSIZE):
        world.append([])
        for cellx in range(SCREENWIDTH // CELLSIZE):
            world[celly].append(Cell(possibletiles,(cellx,celly)))

    
    startcell = world[0][0]
    startcell.tile = RandomTileFromPossible(startcell)
    print(startcell.tile.name)
    #repeat these steps
    Propogate(startcell,world)
    #observe next cell
    #repeat until world done



