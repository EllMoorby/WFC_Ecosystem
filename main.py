from eventManager import EventManager
import sys
import cProfile
from gui import GUI, int_callback

eventManager = EventManager() #Start a new event manager
eventManager.TempMapViewer()
sys.setrecursionlimit(6**10)
gui = GUI()
gui.mainloop()

"""with cProfile.Profile() as pr:
    eventManager.Main(pr) #Begin the main program"""