from constants import *
import json
import random
from pygame import image,transform
from os import path


class Tile:
    def __init__(self,imgpath,name,adjacencylist,bias,weight,traversable,fertile,cellsize) -> None:
        self.img = transform.scale(image.load(path.join(TILES_FOLDER,imgpath)).convert_alpha(),(cellsize,cellsize)) #png of file
        self.adjacencylist = adjacencylist #List of other tile objects allowed to TOUCH
        self.name = name
        self.bias = {}
        self.tempbias = bias #bias
        self.weight = weight
        self.traversable = traversable
        self.fertile = fertile
    
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
        self.tile = None #current tile
        self.bias = {} #current cell bias
        self.hasBerry = False #whether the cell has a Berry
        self.hasTarget = False #whether the cell has a creature targeting it
        self.target = None
        for item in self.possibletiles:
            self.bias[item] = 1

    def __cmp__(self, other):
        if len(self.possibletiles) > len(other.possibletiles):
            return 1
        elif len(self.possibletiles) == len(other.possibletiles):
            return 0
        else: return -1 #comparing two cells compares the size of possible tiles
    
    def __str__(self):
        return self.tile.name[0] #when called, the first letter of the tile is returned

def PrintWorld(world): #prints the current world in console
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


def GetAdjacencyList(tilelist): #translates the adjacency list in the JSON file into a list of objects instead of names

    for tiles in tilelist:
        for index,tilename in enumerate(tiles.adjacencylist):
            for tile in tilelist:
                if tilename == tile.name:
                    tiles.adjacencylist[index] = tile


    

    return tilelist

def Observe(world,possibletiles): #find the cell with the lowsest number of possible tiles
    cells = {}
    for row in world:
        for cell in row:
            if len(cell.possibletiles) != 0: #if the tile has not been set
                if len(cell.possibletiles) not in cells:
                    cells[len(cell.possibletiles)] = [cell]
                    
                else:
                    cells[len(cell.possibletiles)].append(cell) #adds possible tile lengths to a dictionary


    if len(cells.keys()) == 0: #if the map is full, return -1, the algorithm is finished
        return -1

    keylist = list(cells.keys())
    keylist.sort() 
    randomkey = random.choices(keylist, weights = WFCWEIGHTS[:len(cells.keys())], k=1) #get a random key based on the number of possible tiles, the lower the amount the higher the chance of it being chosen

    randomcell = random.choice(cells[randomkey[0]])
    weightlist = []
    tempdict = {}
    for tile in possibletiles:
        for bias in randomcell.bias:
            if tile.name == bias.name:
                tempdict[tile] = randomcell.bias[bias] 


    # a tile is chosen depending on what tiles the cell is surrounded by. These weights are decided by the JSON file
    for item in tempdict:
        for tile in randomcell.possibletiles:
            if item.name == tile.name:
                weightlist.append(tile.weight*tempdict[item])
    randomcell.tile = random.choices(randomcell.possibletiles,weights=weightlist,k=1)[0]

    return randomcell
    

def UpdateBias(origincell,newcell): #update the bias of a cell depending on the weights of the origin cell
    for item in newcell.bias:
        newcell.bias[item] = max(min(origincell.tile.bias[item]*newcell.bias[item],MAXWEIGHT),MINWEIGHT)
    

def Collapse(origincell,newcell): #collapses adjacent cell's possible tiles depending on what the origin cell's tile is
    originadjacencylist = origincell.tile.adjacencylist
    newpossibletiles = []
    for item in newcell.possibletiles: 
        if item in originadjacencylist:
            newpossibletiles.append(item)
    newcell.possibletiles = newpossibletiles #appends new possible tiles so they reflect the adjacency list of the origin cell

    return len(newcell.possibletiles)==0 and newcell.tile == None



def Propogate(cell,world,screenwidth,cellsize,screenheight):
    for y in range(-1,2):
        for x in range(-1,2):
            try:
                if x==y==0 or not(0 <= cell.position[0]+x <= ((screenwidth // cellsize)-1)) or not(0 <= cell.position[1]+y <= ((screenheight // cellsize)-1)):
                    raise ValueError
                UpdateBias(cell,world[cell.position[0]+x][cell.position[1]+y]) #update biases for the adjacent cell depending on the origin cell
                if Collapse(cell,world[cell.position[0]+x][cell.position[1]+y]):#collapse items not in the tiles adjacencylist from the other cells possible tiles
                     return -1
            except:
                pass
    return world

    

def RandomTileFromPossible(cell):
    return random.choice(cell.possibletiles) #chooses a random tile out of possible tiles
    
def GetPossibleTiles(cellsize): #reads the JSON file
    tilelist = []
    with open(path.join(TILES_FOLDER,"textures.json")) as f: #opens a JSON file
        data = json.load(f)
        for tile in data["tiles"]:
            tilelist.append(Tile(tile["image"],tile["name"],tile["adjacency"],tile["bias"],tile["weight"],tile["traversable"],tile["fertile"],cellsize)) #appends data from file into a tile object

    for tile in tilelist:
        tile.UpdateTilelist(tilelist) #updates the tile list from a list of strings to a list of tile objects
    return tilelist

def WFC(world,possibletiles,cellsize,screenheight,screenwidth): #the main wave function collapse algorithm
    cell = Observe(world,possibletiles) #choose a cell
    if cell ==-1:
        return -1,-1 #if program has finished return
    cell.possibletiles = []
    cell.bias = cell.tile.bias
    world = Propogate(cell,world,screenwidth,cellsize,screenheight) #propogate information from the cell to the surrounding cells
    if world == -1: return -1,-1
    else: return world, possibletiles





def GenerateMap(cellsize,screenheight,screenwidth):
    possibletiles = GetAdjacencyList(GetPossibleTiles(cellsize)) #gets the tileset for the map #####GROUP A - List Operations ########
    tilelist = possibletiles
    world = []
    #generate the world with cell objects
    for cellx in range(screenwidth // cellsize):
        world.append([])
        for celly in range(screenheight // cellsize):
            world[cellx].append(Cell(possibletiles.copy(),(cellx,celly))) #####GROUP B - Multi-dimensional array ########
    #runs the WFC algorithm for each cell object, ensuring every cell has a tile 
    for row in world:
        for cell in row:
            world,possibletiles = WFC(world,possibletiles.copy(),cellsize,screenheight,screenwidth)
            if world == -1: #if the there was a collision, regenerate the map
                return GenerateMap(cellsize,screenheight,screenwidth)
    return world,tilelist



