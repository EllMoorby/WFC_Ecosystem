import tkinter as tk

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Main Menu")
        self.geometry("880x880")
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        frame = MainMenu(container, self)
        self.frames[MainMenu] = frame
        frame.grid(row=0,column=0)
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.active_frame = frame
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        menutext = tk.Label(self,text="Ecosystem Simulator+")
        menutext.grid(row=0,column=0)

        
