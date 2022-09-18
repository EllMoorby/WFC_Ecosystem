import pygame
from eventManager import EventManager
from waveFunctionCollapse import *
from constants import *
from engine import Engine
from renderer import Renderer
from ecosystem import Prey
from pathfinder import PathFinder
import sys
from eventManager import EventManager

sys.setrecursionlimit(6**10)


eventManager = EventManager()
eventManager.Main()



