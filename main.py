from eventManager import EventManager
from waveFunctionCollapse import *
from constants import *
import sys
import cProfile
import snakeviz
from eventManager import EventManager

sys.setrecursionlimit(6**10)
eventManager = EventManager() #Start a new event manager
with cProfile.Profile() as pr:
    eventManager.Main(pr) #Begin the main program



