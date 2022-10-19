from eventManager import EventManager
from waveFunctionCollapse import *
from constants import *
import sys
import cProfile
from gui import GUI

sys.setrecursionlimit(6**10)
"""gui = GUI()
gui.mainloop()"""
eventManager = EventManager() #Start a new event manager

with cProfile.Profile() as pr:
    eventManager.Main(pr) #Begin the main program