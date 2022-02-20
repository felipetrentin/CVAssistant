import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import widgets
import dicts

class Page(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, parent=None):
        Page.__init__(self, parent)
        self.label = tk.Label(self, text="This is page 1")
        self.proj = widgets.Projector(self)
        self.ac1 = widgets.AC(self, topic="ac1/temp", name="ac da porta")
        self.ac2 = widgets.AC(self, topic="ac2/temp", name="ac do final")
        self.label.place(x=0, y=0)
        self.proj.place(x=500, y=0)
        self.ac1.place(x=0, y=100)
        self.ac2.place(x=0, y=500)
        self.clock = widgets.Clock(self)
        self.clock.configure(bg='black',fg='white',font=("arial",40))
        self.clock.place(relx=0.8, relwidth=0.2, y=0)
    def stop(self):
        self.ac1.stop()
        self.ac2.stop()

class Page2(Page):
    def __init__(self, parent=None):
        Page.__init__(self, parent)
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

class Page3(Page):
    def __init__(self, parent=None):
        Page.__init__(self, parent)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.p3 = Page3(self)
        buttonframe = tk.Frame(self, width=120, bg="#ababab", bd=2)
        container = tk.Frame(self)
        buttonframe.pack(side="left", fill="both", expand=False)
        container.pack(side="right", fill="both", expand=True)
        b1 = tk.Button(buttonframe, text="Page 1", command=self.p1.show)
        b2 = tk.Button(buttonframe, text="Page 2", command=self.p2.show)
        b3 = tk.Button(buttonframe, text="Page 3", command=self.p3.show)
        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        b1.place(height=100, width=100, x=10, y=10)
        b2.place(height=100, width=100, x=10, y=120)
        b3.place(height=100, width=100, x=10, y=230)
        
        self.p1.show()
    def stop(self):
        self.p1.stop()
