import tkinter as tk
from eventManager import EventManager
import tkinter.font
import tkinter.ttk as tkk
from constants import *
import json
import os
import matplotlib.pyplot as plt

def int_callback(entry):
    if entry == "":
        return True
    try:
        int(entry)
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
            self.presetdata = json.load(f)
            self.preycount = self.presetdata["PREYCOUNT"]
            self.baseenergyprey = self.presetdata["BASE_ENERGY_PREY"]
            self.mindeathageprey = self.presetdata["MINDEATHAGE_PREY"]
            self.maxdeathageprey = self.presetdata["MAXDEATHAGE_PREY"]
            self.timebetweenprey = self.presetdata["TIMEBETWEENMATES_PREY"]
            self.energylprey = self.presetdata["ENERGYLOSSPERSTEP_PREY"]
            self.predatorcount = self.presetdata["PREDATORCOUNT"]
            self.baseenergypredator = self.presetdata["BASE_ENERGY_PREDATOR"]
            self.mindeathagepredator = self.presetdata["MINDEATHAGE_PREDATOR"]
            self.maxdeathagepredator = self.presetdata["MAXDEATHAGE_PREDATOR"]
            self.timebetweenpredator = self.presetdata["TIMEBETWEENMATES_PREDATOR"]
            self.energylpredator = self.presetdata["ENERGYLOSSPERSTEP_PREDATOR"]
            self.berryconst = self.presetdata["BERRYCONST"]
            self.maxwander = self.presetdata["MAXWANDERDIST"]

        with open(path.join("Settings","settings.json"), "r") as d:
            self.settingsdata = json.load(d)
            self.fps = self.settingsdata["FPS"]
            self.screenwidth = self.settingsdata["SCREENWIDTH"]
            self.screenheight = self.settingsdata["SCREENHEIGHT"]
            self.cellsize = self.settingsdata["CELLSIZE"]
            


    def show_frame(self, cont):
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()

    def clear_widgets(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def Quit(self,event=None):
        self.settingsdata["FPS"] = self.fps
        self.settingsdata["SCREENWIDTH"] = self.screenwidth
        self.settingsdata["SCREENHEIGHT"] = self.screenheight
        self.settingsdata["CELLSIZE"] = self.cellsize
        with open(path.join("Settings","settings.json"), "w") as q:
            json.dump(self.settingsdata,q)
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

        quit_ = tk.Button(self,text="Quit",command=lambda: self.Quit(controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        quit_.grid(row=4,column=0)

    def MovetoSimulationMenu(self,parent,controller):
        controller.clear_widgets(self)
        frame = CreateSimulationMenu(parent, controller)
        controller.frames[CreateSimulationMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(CreateSimulationMenu)

    def LoadtoSimulationMenu(self,parent,controller):
        controller.clear_widgets(self)
        frame = LoadSimulation(parent, controller)
        controller.frames[LoadSimulation] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(LoadSimulation)

    def Settings(self,parent,controller):
        controller.clear_widgets(self)
        frame = Settings(parent, controller)
        controller.frames[Settings] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(Settings)

    def Quit(self,controller):
        controller.settingsdata["FPS"] = controller.fps
        controller.settingsdata["SCREENWIDTH"] = controller.screenwidth
        controller.settingsdata["SCREENHEIGHT"] = controller.screenheight
        controller.settingsdata["CELLSIZE"] = controller.cellsize
        with open(path.join("Settings","settings.json"), "w") as q:
            json.dump(controller.settingsdata,q)
        quit()

    



class CreateSimulationMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)
        self.rowconfigure(12, weight=4)
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

        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="flat",font = controller.guifont,activebackground="#9d9898",width = 5,background="#f27e10")
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
        wanderdistentry = tk.Entry(self, textvariable=MaxWanderDistance, validate="key",validatecommand=(controller.validint,"%P"),relief="flat")
        wanderdistentry.grid(row=8,column=1,padx=(5,25))
        
        berrylabel = tk.Label(self,text="Berry Number",font = controller.guifont)
        berrylabel.grid(row=9,column=0)
        berryentry = tk.Entry(self, textvariable=berryConst, validate="key",validatecommand=(controller.validint,"%P"),relief="flat")
        berryentry.grid(row=9,column=1,padx=(5,25))

        viewerbutton = tk.Button(self,text="Open World Viewer",background="#b8b8b8",command=lambda: self.OpenViewer(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        viewerbutton.grid(row=8,column=3,columnspan=2)

        graphbutton = tk.Button(self,text="Show Population Graph",background="#b8b8b8",command=lambda: self.ShowPopulationGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        graphbutton.grid(row=10,column=3,columnspan=2)

        genegraphbutton = tk.Button(self,text="Show Gene Graph",background="#b8b8b8",command=lambda: self.ShowGeneGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        genegraphbutton.grid(row=11,column=3,columnspan=2)

        startbutton = tk.Button(self,text="Start Simulation",background="#51e41e",relief="flat",command=lambda: self.StartSimulation(parent,controller,preyCountEntry,predatorCountEntry,preyBaseEnergyEntry,preyMinDeathage,preyMaxDeathage,preyEnergyLoss,predatorBaseEnergy,predatorMinDeathage,predatorMaxDeathage,predatorEnergyLoss,berryentry,wanderdistentry,preyTBMEntry,predatorTBMEntry),font = controller.guifont,activebackground="#9d9898",width = 20)
        startbutton.grid(row=12,column=0,columnspan=5)

        savebutton = tk.Button(self,text="Save Parameters",background="#b8b8b8",command=lambda: self.SaveSimulation(parent,controller,preyCountEntry,predatorCountEntry,preyBaseEnergyEntry,preyMinDeathage,preyMaxDeathage,preyEnergyLoss,predatorBaseEnergy,predatorMinDeathage,predatorMaxDeathage,predatorEnergyLoss,berryentry,wanderdistentry,preyTBMEntry,predatorTBMEntry),font = controller.guifont,activebackground="#9d9898",width = 20,relief="groove")
        savebutton.grid(row=9,column=3,columnspan=2)

        checkbox = tk.Checkbutton(self,text="Genes",onvalue=True,offvalue=False,font=controller.guifont,width=10)
        checkbox.grid(row=10,column=0,columnspan=2)

    def Back(self,parent,controller):
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)

    def ShowGeneGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.gestationGeneSizePrey_preframe == []:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        plt.plot(controller.eventManager.gestationGeneSizePrey_preframe,label="Prey",color="b")
        plt.plot(controller.eventManager.gestationGeneSizePredator_preframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Strength Of Gene")
        plt.legend()
        plt.show()

    def ShowPopulationGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.preyListLength_perframe == [] or controller.eventManager.predatorListLength_perframe == []:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        plt.plot(controller.eventManager.preyListLength_perframe,label="Prey",color="b")
        plt.plot(controller.eventManager.predatorListLength_perframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Amount of Creatures")
        plt.legend()
        plt.show()

    def OpenViewer(self,parent,controller):
        controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
        controller.eventManager.TempMapViewer()

    def StartSimulation(self,parent,controller,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM):
        controller.eventManager.InitializeValues(int(preycount.get()),int(predatorcount.get()),int(baseenergyprey.get()),int(mindeathageprey.get()),int(maxdeathageprey.get()),int(energylprey.get()),int(baseenergypredator.get()),int(mindeathagepredator.get()),int(maxdeathagepredator.get()),int(energylpredator.get()),float(berryconst.get()),int(maxwander.get()),int(preyTBM.get()),int(predatorTBM.get()))
        controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
        controller.eventManager.Main()

    def SaveSimulation(self,parent,controller,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM):
        popup = tk.Tk()
        popup.title("Save")
        popup.geometry("200x200")

        savename = tk.StringVar(value="save1")

        savenameLabel = tk.Label(popup,text="Save Name",font = controller.guifont)
        savenameLabel.grid(row=0,column=0)
        savenameEntry = tk.Entry(popup,textvariable=savename)
        savenameEntry.grid(row=0,column=1,padx=(15,5))

        savebutton = tk.Button(popup,text="Save",command=lambda: self.Save(popup,controller,savenameEntry,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
        savebutton.grid(row=1,column=0)
        savebutton = tk.Button(popup,text="Cancel",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
        savebutton.grid(row=1,column=1)

        popup.mainloop()

    def Save(self,popup,controller,savename,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM):
        controller.preycount = int(preycount.get())
        controller.baseenergyprey = int(baseenergyprey.get())
        controller.mindeathageprey = int(mindeathageprey.get())
        controller.maxdeathageprey = int(maxdeathageprey.get())
        controller.timebetweenprey = int(preyTBM.get())
        controller.energylprey = int(energylprey.get())
        controller.predatorcount = int(predatorcount.get())
        controller.baseenergypredator = int(baseenergypredator.get())
        controller.mindeathagepredator = int(mindeathagepredator.get())
        controller.maxdeathagepredator = int(maxdeathagepredator.get())
        controller.timebetweenpredator = int(predatorTBM.get())
        controller.energylpredator = int(energylpredator.get())
        controller.berryconst = float(berryconst.get())
        controller.maxwander = int(maxwander.get())
        savename = savename.get()
        savename = savename + ".json"
        controller.presetdata["PREYCOUNT"] = controller.preycount
        controller.presetdata["BASE_ENERGY_PREY"] = controller.baseenergyprey
        controller.presetdata["MINDEATHAGE_PREY"] = controller.mindeathageprey
        controller.presetdata["MAXDEATHAGE_PREY"] = controller.maxdeathageprey
        controller.presetdata["TIMEBETWEENMATES_PREY"] = controller.timebetweenprey
        controller.presetdata["ENERGYLOSSPERSTEP_PREY"] = controller.energylprey
        controller.presetdata["PREDATORCOUNT"] = controller.predatorcount
        controller.presetdata["BASE_ENERGY_PREDATOR"] = controller.baseenergypredator
        controller.presetdata["MINDEATHAGE_PREDATOR"] = controller.mindeathagepredator
        controller.presetdata["MAXDEATHAGE_PREDATOR"] = controller.maxdeathagepredator
        controller.presetdata["TIMEBETWEENMATES_PREDATOR"] = controller.timebetweenpredator
        controller.presetdata["ENERGYLOSSPERSTEP_PREDATOR"] = controller.energylpredator
        controller.presetdata["BERRYCONST"] = controller.berryconst
        controller.presetdata["MAXWANDERDIST"] = controller.maxwander
        if savename != "preset.json":
            with open(path.join("Saves",savename), "w") as save:
                json.dump(controller.presetdata,save)

        self.Close(popup)


        

    def Close(self, tkinter):
        tkinter.destroy()


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
        fpsLabel.grid(row=4,column=0)
        fpsEntry = tk.Entry(self, textvariable=fps, validate="key",validatecommand=(controller.validint,"%P"))
        fpsEntry.grid(row=4,column=1,padx=(15,5))

    def Back(self,parent,controller,cellsizeEntry,screenWidthEntry,screenHeightEntry,fpsEntry):
        controller.cellsize = int(cellsizeEntry.get())
        controller.screenwidth = int(screenWidthEntry.get())
        controller.screenheight = int(screenHeightEntry.get())
        controller.fps = int(fpsEntry.get())
        controller.eventManager.InitializeSettings(controller.screenheight,controller.screenwidth,controller.cellsize,controller.fps)
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)


class LoadSimulation(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)

        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 5)
        backbutton.grid(row=30,column=7)

        menuText = tk.Label(self,text="Load Simulation",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=2)

        filelist = [fname for fname in os.listdir(SAVES_FOLDER) if fname.endswith('.json')]

        optmenu = tkk.Combobox(self, values=filelist, state='readonly',textvariable="Choose a Save",font=controller.guifont)
        optmenu.grid(row=1,column=0)
        runbutton = tk.Button(self,text="Run",command=lambda: self.Run(parent,controller,optmenu.get()),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 5)
        runbutton.grid(row=2,column=0)

        graphbutton = tk.Button(self,text="Show Population Graph",background="#b8b8b8",command=lambda: self.ShowPopulationGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        graphbutton.grid(row=3,column=0)

    def Back(self,parent,controller):
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)
    
    def Run(self,parent,controller,option):
        option = str(option)
        with open(path.join("Saves",option),"r") as f:
            self.presetdata = json.load(f)
            self.preycount = self.presetdata["PREYCOUNT"]
            self.baseenergyprey = self.presetdata["BASE_ENERGY_PREY"]
            self.mindeathageprey = self.presetdata["MINDEATHAGE_PREY"]
            self.maxdeathageprey = self.presetdata["MAXDEATHAGE_PREY"]
            self.timebetweenprey = self.presetdata["TIMEBETWEENMATES_PREY"]
            self.energylprey = self.presetdata["ENERGYLOSSPERSTEP_PREY"]
            self.predatorcount = self.presetdata["PREDATORCOUNT"]
            self.baseenergypredator = self.presetdata["BASE_ENERGY_PREDATOR"]
            self.mindeathagepredator = self.presetdata["MINDEATHAGE_PREDATOR"]
            self.maxdeathagepredator = self.presetdata["MAXDEATHAGE_PREDATOR"]
            self.timebetweenpredator = self.presetdata["TIMEBETWEENMATES_PREDATOR"]
            self.energylpredator = self.presetdata["ENERGYLOSSPERSTEP_PREDATOR"]
            self.berryconst = self.presetdata["BERRYCONST"]
            self.maxwander = self.presetdata["MAXWANDERDIST"]
        
        controller.eventManager.InitializeValues(self.preycount,self.predatorcount,self.baseenergyprey,self.mindeathageprey,self.maxdeathageprey,self.energylprey,self.baseenergyprey,self.mindeathagepredator,self.maxdeathagepredator,self.energylpredator,self.berryconst,self.maxwander,self.timebetweenprey,self.timebetweenpredator)
        controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
        controller.eventManager.Main()

    def ShowGeneGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.gestationGeneSizePrey_preframe == []:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        plt.plot(controller.eventManager.gestationGeneSizePrey_preframe,label="Prey",color="b")
        plt.plot(controller.eventManager.gestationGeneSizePredator_preframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Strength Of Gene")
        plt.legend()
        plt.show()

    def ShowPopulationGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.preyListLength_perframe == [] or controller.eventManager.predatorListLength_perframe == []:
            return
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        plt.plot(controller.eventManager.preyListLength_perframe,label="Prey",color="b")
        plt.plot(controller.eventManager.predatorListLength_perframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Amount of Creatures")
        plt.legend()
        plt.show()



