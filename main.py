import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import pages
import threading

if __name__ == "__main__":
    root = tk.Tk()
    root.title("JARVIS BETA")
    root.attributes('-fullscreen', True)
    root.config(background="#FF0000")
    main = pages.MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
    main.stop()
