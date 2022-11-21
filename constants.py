from os import path

  
WFCWEIGHTS = [100,30,10,5,1,1] #Weights for Wave Function Collapse placement
MAXWEIGHT = 100000 #Maximum weight for Wave Function Collapse placement
MINWEIGHT = 0.0000001 #Minimum weight for Wave Function Collapse placement
MAIN_FOLDER = path.dirname(__file__) #Main directory
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets") #Asset folder directory
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles") #Tile folder directory
CREATURE_FOLDER = path.join(ASSETS_FOLDER, "creatures") #Creature folder directory
SAVES_FOLDER = path.join(MAIN_FOLDER, "Saves") #Saves folder directory
BERRYIMG = path.join(ASSETS_FOLDER, "objects", "berrybush.png") #Berry image directory
NONTRAVERSABLE_MOVEMENT_MODIFYER = 1000000 #Amount added to non traversable tiles when pathfinding

MAXWANDERDISTANCE = 10 #Maximum distance a creature can wander
MULTI = 0.1 #Prey urge multiplier
BASECHOICEWEIGHTS = [10,1,1] #Eat,wander,reproduce
MAXCHOICEWEIGHT = 300 #Maximum weight weight for activity choice

URGELOSSPERSTEP = 5 #Urge lost per step
SEXLIST = ["m","f"] #List of all sexes

#Prey
MAXOFFSPRING_PREY = 7 #Maximum offspring
MINOFFSPRING_PREY = 3 #Minimum offspring
URGE_REPRODUCE_PREY = 500 #Urge to reproduce
MINREPROAGE_PREY = 50 #Minimum age of reproduction
TIMEBETWEENMATESRANGE = 500 #Time between mates
MINREPROAGERANGE = 10 #Minimum reproduction range


#Predator
URGE_REPRODUCE_PREDATOR = 200 #Urge to reproduce
MINREPROAGE_PREDATOR = 50 #Minimum age of reproduction
URGETOEATRANGE = 40 #Urge to eat range
