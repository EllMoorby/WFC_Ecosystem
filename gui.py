import tkinter as tk
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
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Main Menu")
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)
        self.validint = self.register(int_callback)
        self.titlefont = tk.font.Font(family = "Bahnschrift", size =40,weight="bold")
        self.textfont = tk.font.Font(family="Helvetica", size=30,weight="bold")
        self.guifont = tk.font.Font(family="Helvetica", size=18)
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

        preyCount = tk.IntVar(value=PREYCOUNT)
        predatorCount = tk.IntVar(value=PREDATORCOUNT)
        preyBaseEnergy = tk.IntVar(value=BASE_ENERGY_PREY)
        predatorBaseEnergy = tk.IntVar(value=BASE_ENERGY_PREDATOR)
        preyMaxDeathage = tk.IntVar(value=MAXDEATHAGE_PREY)
        predatorMaxDeathage = tk.IntVar(value=MAXDEATHAGE_PREDATOR)

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
        preyMaxDeathageLabel.grid(row=2,column=0)
        preyMaxDeathageEntry = tk.Entry(self, textvariable=preyMaxDeathage, validate="key",validatecommand=(controller.validint,"%P"))
        preyMaxDeathageEntry.grid(row=2,column=1,padx=(5,25))

        predatorMaxDeathageLabel = tk.Label(self,text="Maximum Predator Death Age",font = controller.guifont)
        predatorMaxDeathageLabel.grid(row=2,column=4)
        predatorMaxDeathageEntry = tk.Entry(self, textvariable=predatorMaxDeathage,validate="key",validatecommand=(controller.validint,"%P"))
        predatorMaxDeathageEntry.grid(row=2,column=3,padx=(25,5))
        

    def Back(self,parent,controller):
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)


class Settings(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)

        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 5)
        backbutton.grid(row=30,column=7)

        menuText = tk.Label(self,text="Settings",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=5)

    def Back(self,parent,controller):
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)
