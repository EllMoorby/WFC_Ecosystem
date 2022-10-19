from os import path
import json

with open(path.join("Saves","temp.json")) as f:
    data = json.load(f)
    fps = data["FPS"]
    screenwidth = data["SCREENWIDTH"]
    screenheight = data["SCREENHEIGHT"]
    cellsize = data["CELLSIZE"]
    preycount = data["PREYCOUNT"]
    baseenergyprey = data["BASE_ENERGY_PREY"]
    mindeathageprey = data["MINDEATHAGE_PREY"]
    maxdeathageprey = data["MAXDEATHAGE_PREY"]
    timebetweenprey = data["TIMEBETWEENMATES_PREY"]
    energylprey = data["ENERGYLOSSPERSTEP_PREY"]
    predatorcount = data["PREDATORCOUNT"]
    baseenergypredator = data["BASE_ENERGY_PREDATOR"]
    mindeathagepredator = data["MINDEATHAGE_PREDATOR"]
    maxdeathagepredator = data["MAXDEATHAGE_PREDATOR"]
    timebetweenpredator = data["TIMEBETWEENMATES_PREDATOR"]
    energylpredator = data["ENERGYLOSSPERSTEP_PREDATOR"]
    berryconst = data["BERRYCONST"]
    maxwander = data["MAXWANDERDIST"]


FPS = fps
SCREENWIDTH = screenwidth
SCREENHEIGHT = screenheight
CELLSIZE = cellsize   
WFCWEIGHTS = [100,30,10,5,1,1]
MAXWEIGHT = 100000
MINWEIGHT = 0.0000001
MAIN_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets")
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles")
CREATURE_FOLDER = path.join(ASSETS_FOLDER, "creatures")
BERRYIMG = path.join(ASSETS_FOLDER, "objects", "berrybush.png")
NONTRAVERSABLE_MOVEMENT_MODIFYER = 1000000
BERRYCONST = berryconst

#Animal Stats
PREYCOUNT = preycount
PREDATORCOUNT = predatorcount

MAXWANDERDISTANCE = 10
MULTI = 0.1
BASECHOICEWEIGHTS = [1,1,1] #eat,wander,reproduce
MAXCHOICEWEIGHT = 300

URGELOSSPERSTEP = 5
SEXLIST = ["m","f"]

#Prey
BASE_ENERGY_PREY = baseenergyprey
MINDEATHAGE_PREY = mindeathageprey
MAXDEATHAGE_PREY = maxdeathageprey
MAXOFFSPRING_PREY = 7
MINOFFSPRING_PREY = 3
URGE_REPRODUCE_PREY = 500
TIMEBETWEENMATES_PREY = timebetweenprey
MINREPROAGE_PREY = 10
BERRYENERGYREFILL = 100
ENERGYLOSSPERSTEP_PREY = energylprey

#Predator
BASE_ENERGY_PREDATOR = baseenergypredator
URGE_REPRODUCE_PREDATOR = 600
TIMEBETWEENMATES_PREDATOR = timebetweenpredator
ENERGYLOSSPERSTEP_PREDATOR = energylpredator
MINDEATHAGE_PREDATOR = mindeathagepredator
MAXDEATHAGE_PREDATOR = maxdeathagepredator
MINREPROAGE_PREDATOR = 100



