import sys
import cProfile
from gui import GUI


sys.setrecursionlimit(6**10)
gui = GUI()
gui.mainloop()

"""with cProfile.Profile() as pr:
    eventManager.Main(pr) #Begin the main program"""