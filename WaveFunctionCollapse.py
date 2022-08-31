from turtle import pos
from constants import *
import json
import random
from pygame import image,transform
from os import path
class Tile:
    def __init__(self,imgpath,name,adjacencylist,bias,weight) -> None:
        self.img = transform.scale(image.load(path.join(TILES_FOLDER,imgpath)).convert_alpha(),(CELLSIZE,CELLSIZE)) #png of file
        self.adjacencylist = adjacencylist #List of other tile objects allowed to TOUCH
        self.name = name
        self.bias = {}
        self.tempbias = bias #bias
        self.weight = weight
    
    def UpdateTilelist(self,tilelist):
        for tile in tilelist:
            self.bias[tile] = 1

        for tile in self.bias:
            for bias in self.tempbias:
                if tile.name == bias:
                    self.bias[tile] = self.tempbias[bias]
                    


class Cell:
    def __init__(self,possibletiles,position) -> None:
        self.position = position
        self.possibletiles = possibletiles # list of possible tiles that changes
        self.tile = None
        self.bias = {}
        for item in self.possibletiles:
            self.bias[item] = 1

    def __cmp__(self, other):
        if len(self.possibletiles) > len(other.possibletiles):
            return 1
        elif len(self.possibletiles) == len(other.possibletiles):
            return 0
        else: return -1
    
    def __str__(self):
        return self.tile.name[0]

class Chunk:
    def __init__(self,cells) -> None:
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)


def PrintWorld(world):
    for row in world:
        print("\n")
        for cell in row:
            try:
                if cell:
                    print(cell)
                else:
                    print("x")
            except:
                print("x",end=" ")

    print("\n")


def GetAdjacencyList(tilelist):

    for tiles in tilelist:
        for index,tilename in enumerate(tiles.adjacencylist):
            for tile in tilelist:
                if tilename == tile.name:
                    tiles.adjacencylist[index] = tile


    

    return tilelist

def Observe(world,possibletiles):
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
    randomkey = random.choices(keylist, weights = WFCWEIGHTS[:len(cells.keys())], k=1)

    randomcell = random.choice(cells[randomkey[0]])
    weightlist = []
    tempdict = {}
    for tile in possibletiles:
        for bias in randomcell.bias:
            if tile.name == bias.name:
                tempdict[tile] = randomcell.bias[bias]



    for item in tempdict:
        for tile in randomcell.possibletiles:
            if item.name == tile.name:
                weightlist.append(tile.weight*tempdict[item])
    randomcell.tile = random.choices(randomcell.possibletiles,weights=weightlist,k=1)[0]

    return randomcell
    

def UpdateBias(origincell,newcell):
    for item in newcell.bias:
        newcell.bias[item] = max(min(origincell.tile.bias[item]*newcell.bias[item],MAXWEIGHT),MINWEIGHT)
    

def Collapse(origincell,newcell):
    originadjacencylist = origincell.tile.adjacencylist
    newpossibletiles = []
    for item in newcell.possibletiles:
        if item in originadjacencylist:
            newpossibletiles.append(item)
    newcell.possibletiles = newpossibletiles

    return len(newcell.possibletiles)==0 and newcell.tile == None



def Propogate(cell,world):
    for y in range(-1,2):
        for x in range(-1,2):
            try:
                if x==y==0 or not(0 <= cell.position[0]+x <= ((SCREENWIDTH // CELLSIZE)-1)) or not(0 <= cell.position[1]+y <= ((SCREENHEIGHT // CELLSIZE)-1)):
                    raise ValueError
                UpdateBias(cell,world[cell.position[0]+x][cell.position[1]+y])
                if Collapse(cell,world[cell.position[0]+x][cell.position[1]+y]):#collapse items not in the tiles adjacencylist from the other cells possible tiles
                     return -1
            except:
                pass
    return world

    

def RandomTileFromPossible(cell):
    return random.choice(cell.possibletiles)
    
def GetPossibleTiles():
    tilelist = []
    with open(path.join(TILES_FOLDER,"textures.json")) as f:
        data = json.load(f)
        for tile in data["tiles"]:
            tilelist.append(Tile(tile["image"],tile["name"],tile["adjacency"],tile["bias"],tile["weight"]))

    for tile in tilelist:
        tile.UpdateTilelist(tilelist)
    return tilelist

def WFC(world,possibletiles):
    cell = Observe(world,possibletiles)
    if cell ==-1:
        return
    cell.possibletiles = []
    cell.bias = cell.tile.bias
    
    world = Propogate(cell,world)
    if world == -1: return
    WFC(world,possibletiles)





def GenerateMap():
    possibletiles = GetAdjacencyList(GetPossibleTiles())
    world = []
    for cellx in range(SCREENWIDTH // CELLSIZE):
        world.append([])
        for celly in range(SCREENHEIGHT // CELLSIZE):
            world[cellx].append(Cell(possibletiles.copy(),(cellx,celly)))
    WFC(world,possibletiles.copy())
    return world
    



