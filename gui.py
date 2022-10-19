import tkinter as tk

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Main Menu")
        self.geometry("880x880")
        self.titlefont = tk.font.Font(family = "Bahnschrift", size =40,weight="bold")
        self.textfont = tk.font.Font(family="Helvetica", size=30,weight="bold")
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        frame = MainMenu(container, self)
        self.frames[MainMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()


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
        frame = CreateSimulationMenu(parent, controller)
        controller.frames[CreateSimulationMenu] = frame
        frame.grid(row=0,column=0,sticky="ns")
        controller.show_frame(CreateSimulationMenu)

    def LoadtoSimulationMenu(self):
        pass

    def Settings(self):
        pass

    def Quit(self):
        quit()


class CreateSimulationMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        print("test")
        menuText = tk.Label(self,text="Ecosystem Simulator+",font = controller.titlefont)
        menuText.grid(row=0,column=0)

        
