import sys
import cProfile
from gui import GUI


sys.setrecursionlimit(6**10) #Set the recursion limit to a large number for pathfinding purposes

gui = GUI() #Create a GUI instance
gui.mainloop() #Start the GUI