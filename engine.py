from time import perf_counter
from pygame.time import Clock

class Engine: #Create an engine class
    def __init__(self,fps):
        self.FPS = fps #Set the FPS
        self.clock = Clock() #Create a pygame clock
        self.t1 = perf_counter() #Set the time the engine was created
    
    def update_dt(self):
        self.clock.tick(self.FPS) #Set clock to current fps
        self.dt = perf_counter() - self.t1 #Work out the time between frames
        self.dt *= 10 #Convert the time between frames to a useful data
        self.t1 = perf_counter() #Set t1 to the current time
