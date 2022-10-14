import tkinter as tk
import tkinter.font
from constants import *

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
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Main Menu")
        self.geometry("1920x1080")
        self.validint = self.register(int_callback)
        self.titlefont = tk.font.Font(family = "Bahnschrift", size =40,weight="bold")
        self.textfont = tk.font.Font(family="Helvetica", size=30,weight="bold")
        self.guifont = tk.font.Font(family="Helvetica", size=18)
        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand=True)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        frame = MainMenu(self.container, self)
        self.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        self.show_frame(MainMenu)


    def show_frame(self, cont):
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()


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
        controller.clear_widgets()
        frame = CreateSimulationMenu(parent, controller)
        controller.frames[CreateSimulationMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(CreateSimulationMenu)

    def LoadtoSimulationMenu(self):
        pass

    def Settings(self,parent,controller):
        controller.clear_widgets()
        frame = Settings(parent, controller)
        controller.frames[Settings] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(Settings)

    def Quit(self):
        quit()


class CreateSimulationMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        preyCount = tk.IntVar(value=PREYCOUNT)
        predatorCount = tk.IntVar(value=PREDATORCOUNT)
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


class Settings(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        menuText = tk.Label(self,text="Settings",font = controller.titlefont)
        menuText.grid(row=0,column=0,columnspan=5)