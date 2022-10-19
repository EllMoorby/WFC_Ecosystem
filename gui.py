from asyncio import constants
import tkinter as tk
from turtle import screensize
from eventManager import EventManager
import tkinter.font
from constants import *

def int_callback(entry, max=None, min=None):
    if entry == "":
        return True
    try:
        int(entry)
        if max is not None and min is not None:
            if entry > max or entry < min:
                return False
            else:return True
    except:
        return False
    else: return True

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.eventManager = EventManager()
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Main Menu")
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)
        self.validint = self.register(int_callback)
        self.titlefont = tk.font.Font(family = "Bahnschrift", size =40,weight="bold")
        self.textfont = tk.font.Font(family="Helvetica", size=30,weight="bold")
        self.guifont = tk.font.Font(family="Bahnschrift", size=18)
        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand=True)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.fullscreen = True
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.Quit)

        self.frames = {}
        frame = MainMenu(self.container, self)
        self.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        self.show_frame(MainMenu)
        with open(path.join("Saves","preset.json"),"r") as f:
            data = json.load(f)
            self.fps = data["FPS"]
            self.screenwidth = data["SCREENWIDTH"]
            self.screenheight = data["SCREENHEIGHT"]
            self.cellsize = data["CELLSIZE"]
            self.preycount = data["PREYCOUNT"]
            self.baseenergyprey = data["BASE_ENERGY_PREY"]
            self.mindeathageprey = data["MINDEATHAGE_PREY"]
            self.maxdeathageprey = data["MAXDEATHAGE_PREY"]
            self.timebetweenprey = data["TIMEBETWEENMATES_PREY"]
            self.energylprey = data["ENERGYLOSSPERSTEP_PREY"]
            self.predatorcount = data["PREDATORCOUNT"]
            self.baseenergypredator = data["BASE_ENERGY_PREDATOR"]
            self.mindeathagepredator = data["MINDEATHAGE_PREDATOR"]
            self.maxdeathagepredator = data["MAXDEATHAGE_PREDATOR"]
            self.timebetweenpredator = data["TIMEBETWEENMATES_PREDATOR"]
            self.energylpredator = data["ENERGYLOSSPERSTEP_PREDATOR"]
            self.berryconst = data["BERRYCONST"]
            self.maxwander = data["MAXWANDERDIST"]

        with open(path.join("Saves","preset.json"),"r") as start, open(path.join("Saves","temp.json"),"w") as to:
            to.write(start.read())
            


    def show_frame(self, cont):
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()

    def clear_widgets(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def Quit(self,event=None):
        quit()

    def toggle_fullscreen(self,event=None):
        if self.fullscreen:
            self.attributes("-fullscreen", False)
            self.fullscreen = False
        else:
            self.attributes("-fullscreen", True)
            self.fullscreen = True

    


class MainMenu(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        buttonwidth = 17
        buttonrelief = "groove"

        menuText = tk.Label(self,text="Ecosystem Simulator+",font = controller.titlefont)
        menuText.grid(row=0,column=0)

        createSimulation = tk.Button(self,text="Create Simulation",command=lambda: self.MovetoSimulationMenu(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        createSimulation.grid(row=1,column=0)

        loadSimulation = tk.Button(self,text="Load Simulation",command=lambda: self.LoadtoSimulationMenu(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        loadSimulation.grid(row=2,column=0)

        settings = tk.Button(self,text="Settings",command=lambda: self.Settings(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        settings.grid(row=3,column=0)

        quit_ = tk.Button(self,text="Quit",command=self.Quit,relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        quit_.grid(row=4,column=0)

    def MovetoSimulationMenu(self,parent,controller):
        controller.clear_widgets(self)
        frame = CreateSimulationMenu(parent, controller)
        controller.frames[CreateSimulationMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(CreateSimulationMenu)

    def LoadtoSimulationMenu(self):
        pass

    def Settings(self,parent,controller):
        controller.clear_widgets(self)
        frame = Settings(parent, controller)
        controller.frames[Settings] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(Settings)

    def Quit(self):
        quit()

    



class CreateSimulationMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)

        preyCount = tk.IntVar(value=controller.preycount)
        predatorCount = tk.IntVar(value=controller.predatorcount)
        preyBaseEnergy = tk.IntVar(value=controller.baseenergyprey)
        predatorBaseEnergy = tk.IntVar(value=controller.baseenergypredator)
        preyMaxDeathage = tk.IntVar(value=controller.maxdeathageprey)
        predatorMaxDeathage = tk.IntVar(value=controller.maxdeathagepredator)
        preyMinDeathage = tk.IntVar(value=controller.mindeathageprey)
        predatorMinDeathage = tk.IntVar(value=controller.mindeathagepredator)
        preyEnergyLoss = tk.IntVar(value=controller.energylprey)
        predatorEnergyLoss = tk.IntVar(value=controller.energylpredator)
        preyTimeBetweenMates = tk.IntVar(value=controller.timebetweenprey)
        predatorTimeBetweenMates = tk.IntVar(value=controller.timebetweenpredator)
        MaxWanderDistance = tk.IntVar(value=controller.maxwander)
        berryConst = tk.IntVar(value=controller.berryconst)

        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 5)
        backbutton.grid(row=30,column=7)

        
        menuText = tk.Label(self,text="Create Simulation",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=5)
        
        preyCountLabel = tk.Label(self,text="Starting Number of Prey",font = controller.guifont)
        preyCountLabel.grid(row=1,column=0)
        preyCountEntry = tk.Entry(self, textvariable=preyCount, validate="key",validatecommand=(controller.validint,"%P"))
        preyCountEntry.grid(row=1,column=1,padx=(5,25))

        predatorCountLabel = tk.Label(self,text="Starting Number of Predators",font = controller.guifont)
        predatorCountLabel.grid(row=1,column=4)
        predatorCountEntry = tk.Entry(self, textvariable=predatorCount,validate="key",validatecommand=(controller.validint,"%P"))
        predatorCountEntry.grid(row=1,column=3,padx=(25,5))

        preyBaseEnergyLabel = tk.Label(self,text="Maxiumum Prey Energy",font = controller.guifont)
        preyBaseEnergyLabel.grid(row=2,column=0)
        preyBaseEnergyEntry = tk.Entry(self, textvariable=preyBaseEnergy, validate="key",validatecommand=(controller.validint,"%P"))
        preyBaseEnergyEntry.grid(row=2,column=1,padx=(5,25))

        predatorBaseEnergyLabel = tk.Label(self,text="Maximum Predator Energy",font = controller.guifont)
        predatorBaseEnergyLabel.grid(row=2,column=4)
        predatorBaseEnergyEntry = tk.Entry(self, textvariable=predatorBaseEnergy,validate="key",validatecommand=(controller.validint,"%P"))
        predatorBaseEnergyEntry.grid(row=2,column=3,padx=(25,5))

        preyMaxDeathageLabel = tk.Label(self,text="Maxiumum Prey Death Age",font = controller.guifont)
        preyMaxDeathageLabel.grid(row=3,column=0)
        preyMaxDeathageEntry = tk.Entry(self, textvariable=preyMaxDeathage, validate="key",validatecommand=(controller.validint,"%P"))
        preyMaxDeathageEntry.grid(row=3,column=1,padx=(5,25))

        predatorMaxDeathageLabel = tk.Label(self,text="Maximum Predator Death Age",font = controller.guifont)
        predatorMaxDeathageLabel.grid(row=3,column=4)
        predatorMaxDeathageEntry = tk.Entry(self, textvariable=predatorMaxDeathage,validate="key",validatecommand=(controller.validint,"%P"))
        predatorMaxDeathageEntry.grid(row=3,column=3,padx=(25,5))
        
        preyMaxDeathageLabel = tk.Label(self,text="Minimum Prey Death Age",font = controller.guifont)
        preyMaxDeathageLabel.grid(row=4,column=0)
        preyMaxDeathageEntry = tk.Entry(self, textvariable=preyMinDeathage, validate="key",validatecommand=(controller.validint,"%P"))
        preyMaxDeathageEntry.grid(row=4,column=1,padx=(5,25))

        predatorMinDeathageLabel = tk.Label(self,text="Minimum Predator Death Age",font = controller.guifont)
        predatorMinDeathageLabel.grid(row=4,column=4)
        predatorMinDeathageEntry = tk.Entry(self, textvariable=predatorMinDeathage,validate="key",validatecommand=(controller.validint,"%P"))
        predatorMinDeathageEntry.grid(row=4,column=3,padx=(25,5))

        preyEnergyLossLabel = tk.Label(self,text="Prey Energy Loss per Step",font = controller.guifont)
        preyEnergyLossLabel.grid(row=5,column=0)
        preyEnergyLossEntry = tk.Entry(self, textvariable=preyEnergyLoss, validate="key",validatecommand=(controller.validint,"%P"))
        preyEnergyLossEntry.grid(row=5,column=1,padx=(5,25))

        predatorEnergyLossLabel = tk.Label(self,text="Predator Energy Loss per Step",font = controller.guifont)
        predatorEnergyLossLabel.grid(row=5,column=4)
        predatorEnergyLossEntry = tk.Entry(self, textvariable=predatorEnergyLoss,validate="key",validatecommand=(controller.validint,"%P"))
        predatorEnergyLossEntry.grid(row=5,column=3,padx=(25,5))

        preyTBMLabel = tk.Label(self,text="Prey Time Between Mates",font = controller.guifont)
        preyTBMLabel.grid(row=6,column=0)
        preyTBMEntry = tk.Entry(self, textvariable=preyTimeBetweenMates, validate="key",validatecommand=(controller.validint,"%P"))
        preyTBMEntry.grid(row=6,column=1,padx=(5,25))

        predatorTBMLabel = tk.Label(self,text="Predator Time Between Mates",font = controller.guifont)
        predatorTBMLabel.grid(row=6,column=4)
        predatorTBMEntry = tk.Entry(self, textvariable=predatorTimeBetweenMates,validate="key",validatecommand=(controller.validint,"%P"))
        predatorTBMEntry.grid(row=6,column=3,padx=(25,5))

        othersTitle = tk.Label(self,text="Other Settings",font = controller.textfont)
        othersTitle.grid(row=7,column=0,columnspan=2)

        wanderdistlabel = tk.Label(self,text="Max Wander Distance",font = controller.guifont)
        wanderdistlabel.grid(row=8,column=0)
        wanderdistentry = tk.Entry(self, textvariable=MaxWanderDistance, validate="key",validatecommand=(controller.validint,"%P"))
        wanderdistentry.grid(row=8,column=1,padx=(5,25))
        
        berrylabel = tk.Label(self,text="Berry Number",font = controller.guifont)
        berrylabel.grid(row=9,column=0)
        berryentry = tk.Entry(self, textvariable=berryConst, validate="key",validatecommand=(controller.validint,"%P"))
        berryentry.grid(row=9,column=1,padx=(5,25))

        viewerbutton = tk.Button(self,text="Open World Viewer",command=lambda: self.OpenViewer(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        viewerbutton.grid(row=8,column=3,columnspan=2)

        startbutton = tk.Button(self,text="Start Simulation",command=lambda: self.StartSimulation(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        startbutton.grid(row=15,column=0,columnspan=5)

    def Back(self,parent,controller):
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)

    def OpenViewer(self,parent,controller):
        controller.eventManager.TempMapViewer()

    def StartSimulation(self,parent,controller):
        

        with open (path.join("Saves","temp.json"),"w") as edit:
            data = json.load(edit)
            """data["FPS"] = controller.fps
            data["SCREENWIDTH"] = controller.screenwidth
            data["SCREENHEIGHT"] = controller.screenheight
            data["CELLSIZE"] = controller.cellsize
            data["PREYCOUNT"] = controller.preycount
            data["BASE_ENERGY_PREY"] = controller.baseenergyprey
            data["MINDEATHAGE_PREY"] = controller.mindeathageprey
            data["MAXDEATHAGE_PREY"] = controller.maxdeathageprey
            data["TIMEBETWEENMATES_PREY"] = controller.timebetweenprey
            data["ENERGYLOSSPERSTEP_PREY"] = controller.energylprey
            data["PREDATORCOUNT"] = controller.predatorcount
            data["BASE_ENERGY_PREDATOR"] = controller.baseenergypredator
            data["MINDEATHAGE_PREDATOR"] = controller.mindeathagepredator
            data["MAXDEATHAGE_PREDATOR"] = controller.maxdeathagepredator
            data["TIMEBETWEENMATES_PREDATOR"] = controller.timebetweenpredator
            data["ENERGYLOSSPERSTEP_PREDATOR"] = controller.energylpredator
            data["BERRYCONST"] = controller.berryconst
            data["MAXWANDERDIST"] = controller.maxwander"""
        controller.eventManager.Main()


class Settings(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)

        fps = tk.IntVar(value=controller.fps)
        screenwidth = tk.IntVar(value=controller.screenwidth)
        screenheight = tk.IntVar(value=controller.screenheight)
        cellsize = tk.IntVar(value=controller.cellsize)

        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller,cellsizeEntry,screenWidthEntry,screenHeightEntry,fpsEntry),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 5)
        backbutton.grid(row=30,column=7)

        menuText = tk.Label(self,text="Settings",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=2)

        screenHeightLabel = tk.Label(self,text="Screen Height",font = controller.guifont)
        screenHeightLabel.grid(row=1,column=0)
        screenHeightEntry = tk.Entry(self, textvariable=screenheight, validate="key",validatecommand=(controller.validint,"%P"))
        screenHeightEntry.grid(row=1,column=1,padx=(15,5))

        screenWidthLabel = tk.Label(self,text="Screen Width",font = controller.guifont)
        screenWidthLabel.grid(row=2,column=0)
        screenWidthEntry = tk.Entry(self, textvariable=screenwidth, validate="key",validatecommand=(controller.validint,"%P"))
        screenWidthEntry.grid(row=2,column=1,padx=(15,5))

        cellsizeLabel = tk.Label(self,text="Cell Size",font = controller.guifont)
        cellsizeLabel.grid(row=3,column=0)
        cellsizeEntry = tk.Entry(self, textvariable=cellsize, validate="key",validatecommand=(controller.validint,"%P"))
        cellsizeEntry.grid(row=3,column=1,padx=(15,5))

        fpsLabel = tk.Label(self,text="FPS",font = controller.guifont)
        fpsLabel.grid(row=1,column=0)
        fpsEntry = tk.Entry(self, textvariable=fps, validate="key",validatecommand=(controller.validint,"%P"))
        fpsEntry.grid(row=1,column=1,padx=(15,5))

    def Back(self,parent,controller,cellsizeEntry,screenWidthEntry,screenHeightEntry,fpsEntry):
        controller.cellsize = cellsizeEntry
        controller.screenwidth = screenWidthEntry
        controller.screenheight = screenHeightEntry
        controller.fps = fpsEntry

        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)
