from constants import *
import json
import random
import numpy as np


class Tile():
    def __init__(self,img,name) -> None:
        self.img = img #png of file
        self.adjacencylist = [] #List of other tiles allowed to TOUCH
        self.name = name

class Cell():
    def __init__(self,possibletiles,position) -> None:
        self.position = position
        self.ALLTILES = possibletiles #neverchange
        self.possibletiles = possibletiles # list of possible tiles that changes
        self.tile = None

    def __cmp__(self, other):
        if len(self.possibletiles) > len(other.possibletiles):
            return 1
        elif len(self.possibletiles) == len(other.possibletiles):
            return 0
        else: return -1
    
    def __str__(self):
        return self.tile.name[0]

class Chunk():
    def __init__(self,cells) -> None:
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)


def PrintWorld(world):
    for row in world:
        print("\n")
        for cell in row:#
            try:
                print(cell,end=" ")
            except:
                print("0",end=" ")
    print("\n")


def GetAdjacencyList(tilelist):
    #temporary
    #"adjacency":["grass","sand"]
    tilelist[0].adjacencylist = [tilelist[0],tilelist[2]]
    #"adjacency":["water","sand"]
    tilelist[1].adjacencylist = [tilelist[1],tilelist[2]]
    #"adjacency":["water","sand","grass"]
    tilelist[2].adjacencylist = [tilelist[0],tilelist[1],tilelist[2]]
    

    return tilelist

def Observe(world):
    cells = {}
    for row in world:
        for cell in row:
            if len(cell.possibletiles) != 0:
                if len(cell.possibletiles) not in cells:
                    cells[len(cell.possibletiles)] = [cell]
                    
                else:
                    cells[len(cell.possibletiles)].append(cell)



    if len(cells.keys()) == 0:
        return -1

    keylist = list(cells.keys())
    keylist.sort()
    randomkey = random.choices(keylist, weights = WEIGHTS[:len(cells.keys())], k=1)
    print(keylist)
    print(randomkey)
    #print(cells[randomkey[0]])
    return random.choice(cells[(randomkey[0])])

    
    


def Collapse(origincell,newcell):
    originadjacencylist = origincell.tile.adjacencylist
    newpossibletiles = newcell.possibletiles
    for item in newpossibletiles:
        if item not in originadjacencylist:
            newpossibletiles.remove(item)
    newcell.possibletiles = newpossibletiles
    """for item in newcell.possibletiles:
        print(item.name)"""

def Propogate(cell,world):
    for y in range(-1,2):
        for x in range(-1,2):
            try:
                if x==y==0 or not(0 <= cell.position[0]+x <= 9) or not(0 <= cell.position[1]+y <= 9):
                    raise ValueError
                Collapse(cell,world[cell.position[0]+x][cell.position[1]+y]) #collapse items not in the tiles adjacencylist from the other cells possible tiles
            except:
                #print("outta range")
                pass
    return world

    

def RandomTileFromPossible(cell):
    return random.choice(cell.possibletiles)
    
def GetPossibleTiles():
    tilelist = []
    with open(path.join(TILES_FOLDER,"textures.json")) as f:
        data = json.load(f)
        for tile in data["tiles"]:
            tilelist.append(Tile(tile["image"],tile["name"]))
    return tilelist

def WFC(world):
    
    cell = Observe(world)
    if cell ==-1:
        return
        
    for item in cell.possibletiles:
        print(item.name,end=" ")
    cell.tile = RandomTileFromPossible(cell)
    print(", choice",cell.tile.name)
    print("coords", cell.position)
    print()
    cell.possibletiles = []
    Propogate(cell,world)
    PrintWorld(world)
    WFC(world)





def GenerateMap():
    possibletiles = GetAdjacencyList(GetPossibleTiles())
    for item in possibletiles:
        print(item.name)
    print("$$$$$$$$$$$$$$$")
    for item in possibletiles:
        for thing in item.adjacencylist:
            print(thing.name)

        print("__________")
    world = []
    for cellx in range(SCREENHEIGHT // CELLSIZE):
        world.append([])
        for celly in range(SCREENWIDTH // CELLSIZE):
            world[cellx].append(Cell(possibletiles.copy(),(cellx,celly)))
    PrintWorld(world)
    WFC(world)
    PrintWorld(world)
    print("\nend")
    



