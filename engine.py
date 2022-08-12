from time import perf_counter
from pygame.time import Clock
from constants import FPS

class Engine:
    def __init__(self):
        self.clock = Clock()
        self.t1 = perf_counter()
    
    def update_dt(self):
        self.clock.tick(FPS)
        self.dt = perf_counter() - self.t1
        self.dt *= 10
        self.t1 = perf_counter()