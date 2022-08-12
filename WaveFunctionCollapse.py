from constants import *
import json


class Tile():
    def __init__(self,img,name) -> None:
        self.img = img #png of file
        self.adjacencylist = [] #List of other tiles allowed to TOUCH
        self.name = name

class Cell():
    def __init__(self,possibletiles) -> None:
        self.possibletiles = possibletiles # list of possible tiles

class Chunk():
    def __init__(self,cells) -> None:
        self.cells = cells

    def __iter__(self):
        return iter(self.cells)


def GetPossibleTiles():
    tilelist = []
    with open(path.join(TILES_FOLDER,"textures.json")) as f:
        data = json.load(f)
        for tile in data["tiles"]:
            tilelist.append(Tile(tile["image"],tile["name"]))

    return tilelist

def GenerateMap():
    possibletiles = GetPossibleTiles()
    world = []
    for celly in range(SCREENHEIGHT // CELLSIZE):
        world.append([])
        for cellx in range(SCREENWIDTH // CELLSIZE):
            world[celly].append(Cell(possibletiles))