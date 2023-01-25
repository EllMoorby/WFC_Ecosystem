import tkinter as tk
from eventManager import EventManager
import tkinter.font
import tkinter.ttk as tkk
from constants import *
import json
import os
import matplotlib.pyplot as plt

def int_callback(entry): #defines a callback function which determines if "entry" is an integer
    if entry == "":
        return True
    try:
        int(entry)
    except:
        return False
    else: return True

def flt_callback(entry): #defines a callback function which determines if "entry" is an integer
    if entry == "":
        return True
    try:
        float(entry)
    except:
        return False
    else: return True


class GUI(tk.Tk): #Main GUI class
    def __init__(self, *args, **kwargs):
        self.eventManager = EventManager() #Start an event manager instance
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Ecosystem Simulation+") #Add a title to the window
        self.geometry("1920x1080") #Set the window size to 1920x1080
        self.attributes("-fullscreen", True) #Set the window to fullscreen
        self.validint = self.register(int_callback) #Register a callback function
        self.validfloat = self.register(flt_callback) #Register a callback function
        self.titlefont = tk.font.Font(family = "Bahnschrift", size =60,weight="bold") #Setup fonts for the text
        self.textfont = tk.font.Font(family="Helvetica", size=30,weight="bold")
        self.guifont = tk.font.Font(family="Bahnschrift", size=18)
        self.errorfont = tk.font.Font(family="Bahnschrift", size=12,weight="bold")
        self.container = tk.Frame(self) #Add a frame
        self.container.pack(side="top",fill="both",expand=True)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.fullscreen = True #Start the window in fullscreen
        self.bind("<F11>", self.toggle_fullscreen) #Bind F11 to toggle_fullscreen
        self.bind("<Escape>", self.Quit) #Bind Escape to quit
        self.bg = tk.PhotoImage(file = path.join(ASSETS_FOLDER,"bg","bg.png"),height = self.winfo_screenheight(),width = self.winfo_screenwidth())
        

        self.frames = {} #######GROUP B - Dictionary ########
        frame = MainMenu(self.container, self)
        self.frames[MainMenu] = frame #Add the frame to the dictionary
        frame.grid(row=0,column=0,sticky="ns")
        self.show_frame(MainMenu) #Show the main menu
        #preload all the attributes from a JSON file
        with open(path.join("Saves","preset.json"),"r") as f: #####GROUP A - JSON ##### #######GROUP B - Reading from files ##### #####GROUP A - Files organised for direct access#####
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

        #preload all the current settings
        with open(path.join("Settings","settings.json"), "r") as d:
            self.settingsdata = json.load(d)
            self.fps = self.settingsdata["FPS"]
            self.screenwidth = self.settingsdata["SCREENWIDTH"]
            self.screenheight = self.settingsdata["SCREENHEIGHT"]
            self.cellsize = self.settingsdata["CELLSIZE"]
            


    def show_frame(self, cont): #show the frame
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()

    def clear_widgets(self,frame): #clear the screen
        if frame.canvas is not None:
            frame.canvas.delete("all")
        else:
            for widget in frame.winfo_children():
                widget.destroy()

    def Quit(self,event=None): #Quit the program
        #Save the settings to the JSON file
        self.settingsdata["FPS"] = self.fps
        self.settingsdata["SCREENWIDTH"] = self.screenwidth
        self.settingsdata["SCREENHEIGHT"] = self.screenheight
        self.settingsdata["CELLSIZE"] = self.cellsize
        with open(path.join("Settings","settings.json"), "w") as q:
            json.dump(self.settingsdata,q)
        quit()

    def toggle_fullscreen(self,event=None): #Toggle the fullscreen
        if self.fullscreen:
            self.attributes("-fullscreen", False)
            self.fullscreen = False
        else:
            self.attributes("-fullscreen", True)
            self.fullscreen = True

    


class MainMenu(tk.Frame): #Main Menu
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        buttonwidth = 17
        buttonrelief = "groove"
        self.canvas = None
        
        self.canvas =tk.Canvas(self,height = self.winfo_screenheight(),width = self.winfo_screenwidth())
        self.canvas.pack(fill="both",expand=True)
        bg = self.canvas.create_image(0,0, anchor="nw", image=controller.bg,)

        menuText = tk.Label(controller,text="Ecosystem Simulator+",font = controller.titlefont) 
        menuText_window = self.canvas.create_text(self.winfo_screenwidth()/2,20,anchor="n",text="Ecosystem Simulator+",font = controller.titlefont)
        #Add main menu buttons to the screen
        createSimulation = tk.Button(controller,text="Create Simulation",command=lambda: self.MovetoSimulationMenu(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        createSimulation_window = self.canvas.create_window(self.winfo_screenwidth()/2,250,anchor="n",window=createSimulation)

        loadSimulation = tk.Button(controller,text="Load Simulation",command=lambda: self.LoadtoSimulationMenu(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        loadSimulation_window = self.canvas.create_window(self.winfo_screenwidth()/2,350,anchor="n",window=loadSimulation)

        settings = tk.Button(controller,text="Settings",command=lambda: self.Settings(parent,controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        settings_window = self.canvas.create_window(self.winfo_screenwidth()/2,450,anchor="n",window=settings)

        quit_ = tk.Button(controller,text="Quit",command=lambda: self.Quit(controller),relief=buttonrelief,font = controller.textfont,activebackground="#9d9898",width = buttonwidth)
        quit_window = self.canvas.create_window(self.winfo_screenwidth()/2,550,anchor="n",window=quit_)



    def MovetoSimulationMenu(self,parent,controller): #Change the frame to the Simulation Menu
        controller.clear_widgets(self)
        frame = CreateSimulationMenu(parent, controller)
        controller.frames[CreateSimulationMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(CreateSimulationMenu)

    def LoadtoSimulationMenu(self,parent,controller): #Change the frame to the LoadSimulation Menu
        controller.clear_widgets(self)
        frame = LoadSimulation(parent, controller)
        controller.frames[LoadSimulation] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(LoadSimulation)

    def Settings(self,parent,controller): #Load the Settings Menu
        controller.clear_widgets(self)
        frame = Settings(parent, controller)
        controller.frames[Settings] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(Settings)

    def Quit(self,controller): #Save the settings and quit the program
        controller.settingsdata["FPS"] = controller.fps
        controller.settingsdata["SCREENWIDTH"] = controller.screenwidth
        controller.settingsdata["SCREENHEIGHT"] = controller.screenheight
        controller.settingsdata["CELLSIZE"] = controller.cellsize
        with open(path.join("Settings","settings.json"), "w") as q: #######GROUP B - Writing to files ########
            json.dump(controller.settingsdata,q)
        quit()

    



class CreateSimulationMenu(tk.Frame): #Define the Create Simulation Menu Frame
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.rowconfigure(30, weight=4) #configure rows and columns so buttons can be placed there
        self.columnconfigure(7, weight=4)
        self.rowconfigure(12, weight=4)
        self.canvas = None
        #set the default values
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
        maxWanderDistance = tk.IntVar(value=controller.maxwander)
        berryConst = tk.IntVar(value=controller.berryconst)
        cyclescount = tk.IntVar(value=0)
        
        #create a back button
        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="flat",font = controller.guifont,activebackground="#9d9898",width = 5,background="#f27e10")
        backbutton.grid(row=30,column=7)

        
        menuText = tk.Label(self,text="Create Simulation",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=5)
        #Add all labels for entry boxes
        #Add Entry boxes for all values
        #They are all gridded accoringly
        preyCountLabel = tk.Label(self,text="Starting Number of Prey",font = controller.guifont)
        preyCountLabel.grid(row=1,column=0)
        preyCountEntry = tk.Entry(self, textvariable=preyCount, validate="key",validatecommand=(controller.validint,"%P"))
        preyCountEntry.grid(row=1,column=1,padx=(5,25))

        predatorCountLabel = tk.Label(self,text="Starting Number of Predators",font = controller.guifont)
        predatorCountLabel.grid(row=1,column=3)
        predatorCountEntry = tk.Entry(self, textvariable=predatorCount,validate="key",validatecommand=(controller.validint,"%P"))
        predatorCountEntry.grid(row=1,column=4,padx=(25,5))

        preyBaseEnergyLabel = tk.Label(self,text="Maxiumum Prey Energy",font = controller.guifont)
        preyBaseEnergyLabel.grid(row=2,column=0)
        preyBaseEnergyEntry = tk.Entry(self, textvariable=preyBaseEnergy, validate="key",validatecommand=(controller.validint,"%P"))
        preyBaseEnergyEntry.grid(row=2,column=1,padx=(5,25))

        predatorBaseEnergyLabel = tk.Label(self,text="Maximum Predator Energy",font = controller.guifont)
        predatorBaseEnergyLabel.grid(row=2,column=3)
        predatorBaseEnergyEntry = tk.Entry(self, textvariable=predatorBaseEnergy,validate="key",validatecommand=(controller.validint,"%P"))
        predatorBaseEnergyEntry.grid(row=2,column=4,padx=(25,5))

        preyMaxDeathageLabel = tk.Label(self,text="Maxiumum Prey Death Age",font = controller.guifont)
        preyMaxDeathageLabel.grid(row=3,column=0)
        preyMaxDeathageEntry = tk.Entry(self, textvariable=preyMaxDeathage, validate="key",validatecommand=(controller.validint,"%P"))
        preyMaxDeathageEntry.grid(row=3,column=1,padx=(5,25))

        predatorMaxDeathageLabel = tk.Label(self,text="Maximum Predator Death Age",font = controller.guifont)
        predatorMaxDeathageLabel.grid(row=3,column=3)
        predatorMaxDeathageEntry = tk.Entry(self, textvariable=predatorMaxDeathage,validate="key",validatecommand=(controller.validint,"%P"))
        predatorMaxDeathageEntry.grid(row=3,column=4,padx=(25,5))
        
        preyMaxDeathageLabel = tk.Label(self,text="Minimum Prey Death Age",font = controller.guifont)
        preyMaxDeathageLabel.grid(row=4,column=0)
        preyMaxDeathageEntry = tk.Entry(self, textvariable=preyMinDeathage, validate="key",validatecommand=(controller.validint,"%P"))
        preyMaxDeathageEntry.grid(row=4,column=1,padx=(5,25))

        predatorMinDeathageLabel = tk.Label(self,text="Minimum Predator Death Age",font = controller.guifont)
        predatorMinDeathageLabel.grid(row=4,column=3)
        predatorMinDeathageEntry = tk.Entry(self, textvariable=predatorMinDeathage,validate="key",validatecommand=(controller.validint,"%P"))
        predatorMinDeathageEntry.grid(row=4,column=4,padx=(25,5))

        preyEnergyLossLabel = tk.Label(self,text="Prey Energy Loss per Step",font = controller.guifont)
        preyEnergyLossLabel.grid(row=5,column=0)
        preyEnergyLossEntry = tk.Entry(self, textvariable=preyEnergyLoss, validate="key",validatecommand=(controller.validint,"%P"))
        preyEnergyLossEntry.grid(row=5,column=1,padx=(5,25))

        predatorEnergyLossLabel = tk.Label(self,text="Predator Energy Loss per Step",font = controller.guifont)
        predatorEnergyLossLabel.grid(row=5,column=3)
        predatorEnergyLossEntry = tk.Entry(self, textvariable=predatorEnergyLoss,validate="key",validatecommand=(controller.validint,"%P"))
        predatorEnergyLossEntry.grid(row=5,column=4,padx=(25,5))

        preyTBMLabel = tk.Label(self,text="Prey Time Between Mates",font = controller.guifont)
        preyTBMLabel.grid(row=6,column=0)
        preyTBMEntry = tk.Entry(self, textvariable=preyTimeBetweenMates, validate="key",validatecommand=(controller.validint,"%P"))
        preyTBMEntry.grid(row=6,column=1,padx=(5,25))

        predatorTBMLabel = tk.Label(self,text="Predator Time Between Mates",font = controller.guifont)
        predatorTBMLabel.grid(row=6,column=3)
        predatorTBMEntry = tk.Entry(self, textvariable=predatorTimeBetweenMates,validate="key",validatecommand=(controller.validint,"%P"))
        predatorTBMEntry.grid(row=6,column=4,padx=(25,5))

        othersTitle = tk.Label(self,text="Other Settings",font = controller.textfont)
        othersTitle.grid(row=7,column=0,columnspan=2)

        wanderdistlabel = tk.Label(self,text="Max Wander Distance",font = controller.guifont)
        wanderdistlabel.grid(row=8,column=0)
        wanderdistentry = tk.Entry(self, textvariable=maxWanderDistance, validate="key",validatecommand=(controller.validint,"%P"),relief="flat")
        wanderdistentry.grid(row=8,column=1,padx=(5,25))
        
        berrylabel = tk.Label(self,text="Berry Number",font = controller.guifont)
        berrylabel.grid(row=9,column=0)
        berryentry = tk.Entry(self, textvariable=berryConst, validate="key",validatecommand=(controller.validfloat,"%P"),relief="flat")
        berryentry.grid(row=9,column=1,padx=(5,25))

        cycleslabel = tk.Label(self,text="Number of cycles (0 for infinite)",font = controller.guifont)
        cycleslabel.grid(row=10,column=0)
        cyclesentry = tk.Entry(self, textvariable=cyclescount, validate="key",validatecommand=(controller.validint,"%P"),relief="flat")
        cyclesentry.grid(row=10,column=1,padx=(5,25))

        #Create a button which displays the world world viewer
        viewerbutton = tk.Button(self,text="Open World Viewer",background="#b8b8b8",command=lambda: self.OpenViewer(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        viewerbutton.grid(row=8,column=3,columnspan=2)
        #Create a button which displays a graph of the population of the previous simulation
        graphbutton = tk.Button(self,text="Show Population Graph",background="#b8b8b8",command=lambda: self.ShowPopulationGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        graphbutton.grid(row=10,column=3,columnspan=2)
        #Create a button which displays a graph of the average gene
        genegraphbutton = tk.Button(self,text="Show Gene Graph",background="#b8b8b8",command=lambda: self.ShowGeneGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        genegraphbutton.grid(row=11,column=3,columnspan=2)
        #Create a button which which retrieves all values from the entry boxes
        startbutton = tk.Button(self,text="Start Simulation",background="#51e41e",relief="flat",command=lambda: self.StartSimulation(parent,controller,preyCountEntry,predatorCountEntry,preyBaseEnergyEntry,preyMinDeathage,preyMaxDeathage,preyEnergyLoss,predatorBaseEnergy,predatorMinDeathage,predatorMaxDeathage,predatorEnergyLoss,berryentry,wanderdistentry,preyTBMEntry,predatorTBMEntry,cyclesentry),font = controller.guifont,activebackground="#9d9898",width = 20)
        startbutton.grid(row=12,column=0,columnspan=5)
        #Create a button which opens a popup window to save the simulation
        savebutton = tk.Button(self,text="Save Parameters",background="#b8b8b8",command=lambda: self.SaveSimulation(parent,controller,preyCountEntry,predatorCountEntry,preyBaseEnergyEntry,preyMinDeathage,preyMaxDeathage,preyEnergyLoss,predatorBaseEnergy,predatorMinDeathage,predatorMaxDeathage,predatorEnergyLoss,berryentry,wanderdistentry,preyTBMEntry,predatorTBMEntry),font = controller.guifont,activebackground="#9d9898",width = 20,relief="groove")
        savebutton.grid(row=9,column=3,columnspan=2)


    def Back(self,parent,controller): #Return to the previous frame
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)

    def ShowGeneGraphs(self,parent,controller): #Show the graph of gene strength
        plt.close("all")
        if controller.eventManager.gestationGeneSizePrey_preframe == [] and controller.eventManager.gestationGeneSizePredator_preframe == []: #if no data is written, program has not been run. Therefore the graph can not be shown
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="No data to plot. Please try to run the simulation.",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)
            return
        fig = plt.figure("Graph of the average gene strength for predator and prey")
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        #plot the gene averages
        plt.plot(controller.eventManager.gestationGeneSizePrey_preframe,label="Prey",color="b")
        plt.plot(controller.eventManager.gestationGeneSizePredator_preframe,label="Predators",color="r")
        #label axes
        plt.xlabel("Number of Frames")
        plt.ylabel("Strength Of Gene")
        plt.ylim(top=100,bottom=0)
        plt.xlim(left=0)
        plt.legend()
        plt.show()

    def ShowPopulationGraphs(self,parent,controller): #display the population of the graphs
        plt.close("all")
        if controller.eventManager.preyListLength_perframe == [] and controller.eventManager.predatorListLength_perframe == []: #if there is no data in either list, the program has never been ran, therefore graph cannpt be shown
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="No data to plot. Please try to run the simulation.",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)
            return
        fig = plt.figure("Graph of the creature count for predator and prey")
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        plt.plot(controller.eventManager.preyListLength_perframe,label="Prey",color="b")
        plt.plot(controller.eventManager.predatorListLength_perframe,label="Predators",color="r")
        #label axes
        plt.xlabel("Number of Frames")
        plt.ylabel("Amount of Creatures")
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.legend()
        plt.show()

    def OpenViewer(self,parent,controller): #Open a viewer of the world
        controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
        controller.eventManager.TempMapViewer()

    def StartSimulation(self,parent,controller,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM,cyclescount):
        passed = False
        #Get all values from entry boxes and send them to the eventManager
        try:
            controller.eventManager.InitializeValues(int(preycount.get()),int(predatorcount.get()),int(baseenergyprey.get()),int(mindeathageprey.get()),int(maxdeathageprey.get()),int(energylprey.get()),int(baseenergypredator.get()),int(mindeathagepredator.get()),int(maxdeathagepredator.get()),int(energylpredator.get()),float(berryconst.get()),int(maxwander.get()),int(preyTBM.get()),int(predatorTBM.get()),int(cyclescount.get()))
            passed = True
        except:
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="Invalid input, please re-enter your data",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)
            pass
        if passed:
            #Get the settings from the JSON file
            controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
            #Run the program
            controller.eventManager.Main()

    def SaveSimulation(self,parent,controller,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM):
        #Open a popup box
        popup = tk.Tk()
        popup.title("Save") #Set the window title
        popup.geometry("280x200") #Set the window size

        savename = tk.StringVar(value="save1")

        #Save Entry box where the name will be inputted
        savenameLabel = tk.Label(popup,text="Save Name",font = controller.guifont)
        savenameLabel.grid(row=0,column=0)
        savenameEntry = tk.Entry(popup,textvariable=savename)
        savenameEntry.grid(row=0,column=1,padx=(15,5))

        #Run the Save function on press of a button
        savebutton = tk.Button(popup,text="Save",command=lambda: self.Save(popup,controller,savenameEntry,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
        savebutton.grid(row=1,column=0)
        #Create a button whwich closes the window
        savebutton = tk.Button(popup,text="Cancel",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
        savebutton.grid(row=1,column=1)

        popup.mainloop()

    def Save(self,popup,controller,savename,preycount,predatorcount,baseenergyprey,mindeathageprey,maxdeathageprey,energylprey,baseenergypredator,mindeathagepredator,maxdeathagepredator,energylpredator,berryconst,maxwander,preyTBM,predatorTBM):
        #assign all values from entry boxes to variables
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
        #create a savename from the name and ".json" extension
        savename = savename.get()
        savename = savename + ".json"
        #Assign the values to the dictionary
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

        #Create a new file from the new dictionary
        if savename != "preset.json":
            with open(path.join("Saves",savename), "w") as save:
                json.dump(controller.presetdata,save)

        self.Close(popup)


        

    def Close(self, tkinter):
        #close the window
        tkinter.destroy()


class Settings(tk.Frame): #Create the settings class
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        #configure rows and columns 
        self.canvas = None
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)
        #Assign variables to attributes in the JSON file
        fps = tk.IntVar(value=controller.fps)
        screenwidth = tk.IntVar(value=controller.screenwidth)
        screenheight = tk.IntVar(value=controller.screenheight)
        cellsize = tk.IntVar(value=controller.cellsize)

        #Add a back button to return to the main menu
        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller,cellsizeEntry,screenWidthEntry,screenHeightEntry,fpsEntry),relief="flat",font = controller.guifont,activebackground="#9d9898",width = 5,background="#f27e10")
        backbutton.grid(row=30,column=7)

        menuText = tk.Label(self,text="Settings",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=2)
        #Labels and buttons for each attribute of settings
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
        #retrieves all data from the entry boxes
        try:
            controller.cellsize = int(cellsizeEntry.get())
            controller.screenwidth = int(screenWidthEntry.get())
            controller.screenheight = int(screenHeightEntry.get())
            controller.fps = int(fpsEntry.get())
            controller.eventManager.InitializeSettings(controller.screenheight,controller.screenwidth,controller.cellsize,controller.fps) #change the values in the event manager
            controller.clear_widgets(self) #clear the screen
            frame = MainMenu(parent, controller)
            controller.frames[MainMenu] = frame
            frame.grid(row=0,column=0,sticky="ns")
            controller.show_frame(MainMenu) #moving back to the main menu
        except:
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="Invalid input, please re-enter your data",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)

    def Close(self, tkinter):
        #close the window
        tkinter.destroy()


class LoadSimulation(tk.Frame): #Create the LoadSimulation class
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.canvas = None
        #configure rows and columns so buttons can be placed
        self.columnconfigure(3,weight=3)
        self.rowconfigure(30, weight=4)
        self.columnconfigure(7, weight=4)
        cyclescount = tk.IntVar(value=0)
        #Back button to return to the main menu
        backbutton = tk.Button(self,text="Back",command=lambda: self.Back(parent,controller),relief="flat",font = controller.guifont,activebackground="#9d9898",width = 5,background="#f27e10")
        backbutton.grid(row=30,column=7)

        menuText = tk.Label(self,text="Load Simulation",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=2)

        #create a list of all JSON files that are in the Saves directory
        filelist = [fname for fname in os.listdir(SAVES_FOLDER) if fname.endswith('.json')]

        #Drop down menu to show all the JSON files in the Saves directory
        optmenu = tkk.Combobox(self, values=filelist, state='readonly',textvariable="Choose a Save",font=controller.guifont)
        optmenu.grid(row=1,column=0)
        #Button which starts the simulation with the values selected
        runbutton = tk.Button(self,text="Run",background="#51e41e",relief="flat",command=lambda: self.Run(parent,controller,optmenu.get(),int(cyclesentry.get())),font = controller.guifont,activebackground="#9d9898",width = 5)
        runbutton.grid(row=1,column=1)
        #Button to display a graph of the population
        graphbutton = tk.Button(self,text="Show Population Graph",background="#b8b8b8",command=lambda: self.ShowPopulationGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        graphbutton.grid(row=2,column=0)
        #Entry for number of cycles
        cycleslabel = tk.Label(self,text="Number of cycles (0 for infinite)",font = controller.guifont)
        cycleslabel.grid(row=5,column=0)
        cyclesentry = tk.Entry(self, textvariable=cyclescount, validate="key",validatecommand=(controller.validint,"%P"),relief="flat")
        cyclesentry.grid(row=5,column=1,padx=(5,25))
        #Button to display a graph of the Gene strength
        genebutton = tk.Button(self,text="Show Gene Graph",background="#b8b8b8",command=lambda: self.ShowGeneGraphs(parent,controller),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 20)
        genebutton.grid(row=2,column=1)

    def Back(self,parent,controller): #Returns to the main menu
        controller.clear_widgets(self)
        frame = MainMenu(parent, controller)
        controller.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(MainMenu)
    
    def Run(self,parent,controller,option,cyclevalue):
        option = str(option)
        #Loads the data from the save into variables
        try:
            with open(path.join("Saves",option),"r") as f: #####GROUP A - Files Organised for direct access ########
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
        
            #Initialize these values into the eventManager
            controller.eventManager.InitializeValues(self.preycount,self.predatorcount,self.baseenergyprey,self.mindeathageprey,self.maxdeathageprey,self.energylprey,self.baseenergyprey,self.mindeathagepredator,self.maxdeathagepredator,self.energylpredator,self.berryconst,self.maxwander,self.timebetweenprey,self.timebetweenpredator,cyclevalue)
            controller.eventManager.InitializeSettings(controller.screenwidth,controller.screenwidth,controller.cellsize,controller.fps)
            #Run the main program
            
        except:
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="Invalid input, please enter a valid save",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)

        controller.eventManager.Main()

    def Close(self, tkinter):
            #close the window
            tkinter.destroy()

    def ShowGeneGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.gestationGeneSizePrey_preframe == [] and controller.eventManager.gestationGeneSizePredator_preframe == []: #Check if data is stored to be graphed. No data means the simulation has not run yet
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="No data to plot. Please try to run the simulation.",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)
            return
        fig = plt.figure("Graph of the average gene strength for predator and prey")
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        #Plot the gene strength data
        plt.plot(controller.eventManager.gestationGeneSizePrey_preframe,label="Prey",color="b")
        plt.plot(controller.eventManager.gestationGeneSizePredator_preframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Strength Of Gene")
        plt.ylim(top=100,bottom=0)
        plt.xlim(left=0)
        plt.legend()
        plt.show()

    def ShowPopulationGraphs(self,parent,controller):
        plt.close("all")
        if controller.eventManager.preyListLength_perframe == [] and controller.eventManager.predatorListLength_perframe == []:#Check if data is stored to be graphed. No data means the simulation has not run yet 
            popup = tk.Tk()
            popup.title("Error") #Set the window title
            popup.geometry("345x100") #Set the window size
            savenameLabel = tk.Label(popup,text="No data to plot. Please try to run the simulation.",font = controller.guifont)
            savenameLabel.grid(row=0,column=0)
            close = tk.Button(popup,text="Close",command=lambda: self.Close(popup),relief="groove",font = controller.guifont,activebackground="#9d9898",width = 7)
            close.grid(row=1,column=0)
            return
        fig = plt.figure("Graph of the creature count for predator and prey")
        ax = fig.add_subplot(1,1,1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        #plot the population graphs
        plt.plot(controller.eventManager.preyListLength_perframe,label="Prey",color="b")
        plt.plot(controller.eventManager.predatorListLength_perframe,label="Predators",color="r")
        plt.xlabel("Number of Frames")
        plt.ylabel("Amount of Creatures")
        plt.legend()
        plt.show()



