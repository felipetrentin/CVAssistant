import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import paho.mqtt.client as mqtt
import dicts
import threading
class Projector(tk.Frame):
    """ Class that adds a remote control widget"""
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        """
        create a new frame, add all the buttons and layout in grid.
        """
        buttonsframe = tk.Frame(self, bg="#ff0000", bd=2)
        label = tk.Label(buttonsframe, text="projetor")
        bup = tk.Button(buttonsframe, width = 2, height = 1)
        bdown = tk.Button(buttonsframe, width = 2, height = 1)
        bleft = tk.Button(buttonsframe, width = 2, height = 1)
        bright = tk.Button(buttonsframe, width = 2, height = 1)
        bok = tk.Button(buttonsframe, width = 2, height = 1)
        bpwr = tk.Button(buttonsframe, width = 2, height = 1)
        binput = tk.Button(buttonsframe, width = 2, height = 1)
        besc = tk.Button(buttonsframe, width = 2, height = 1)
        label.grid(row=0, column=0, columnspan=3)
        bup.grid(row=2, column=1)
        bdown.grid(row=4, column=1)
        bleft.grid(row=3, column=0)
        bright.grid(row=3, column=2)
        bpwr.grid(row=1, column=1)
        binput.grid(row=1, column=0)
        besc.grid(row=1, column=2)
        bok.grid(row=3, column=1)
        buttonsframe.pack(side="top")

class AC(tk.Frame):
    """ class to control the AC and do MQTT pubsub"""
    Font_temp = ("OCR A Std", 80, "bold")
    def __init__(self, parent=None, name="This is AC", topic="ac1/temp", hostname="localhost", port=1883):
        tk.Frame.__init__(self, parent)
        #define screen parts
        buttonsframe = tk.Frame(self, bg="#f5a442", bd=2)
        label = tk.Label(buttonsframe, text=name)
        self.templbl = tk.Label(buttonsframe, text=("--ºc"), font=self.Font_temp)
        modecombo = ttk.Combobox(buttonsframe, state="readonly", values = ["auto", "cool", "heat", "fan"])
        fancombo = ttk.Combobox(buttonsframe, state="readonly", values = ["auto", "low", "medium", "high", "quiet"])
        self.uparrow = tk.PhotoImage(file='./res/yellowup.png').subsample(5, 5)
        bup = tk.Button(buttonsframe, image=self.uparrow, command= lambda: self.changeby(1))
        bdown = tk.Button(buttonsframe, height=2, width=5,command= lambda: self.changeby(-1))
        #place parts
        label.grid(row=0, column=0, pady=2,columnspan=2)
        self.templbl.grid(row=1, column=0, pady=2,rowspan=2)
        modecombo.grid(row=3, column=0, padx=2)
        fancombo.grid(row=3, column=1, padx=2)
        bup.grid(row=1, column=1, padx=2)
        bdown.grid(row=2, column=1, padx=2)
        buttonsframe.pack(side="top")
        #connect to MQTT
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async(hostname, port, 60)
        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        print("%s Connected with result code %s" % (self.topic, str(rc)))
        client.subscribe(self.topic)
        
    def on_message(self, client, userdata, msg):
        if(msg.topic == self.topic):
            dicts.topics[self.topic] = int(msg.payload)
            self.templbl.configure(text="{:.0f}ºc".format(dicts.topics[self.topic]))
        print("topic: %s payload: %s " % (msg.topic, str(msg.payload)))

    def changeby(self, value):
        dicts.topics[self.topic] = dicts.topics[self.topic] + value
        self.client.publish(topic = self.topic, payload=(dicts.topics[self.topic]), retain=True)
    
    def stop(self):
        self.client.loop_stop(force=False)
    
class Clock(tk.Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None):
        """
        Create and place the clock widget into the parent element
        It's an ordinary Label element with two additional features.
        """
        tk.Label.__init__(self, parent)
        
        self.time = time.strftime('%e/%m %H:%M:%S')
        self.display_time = self.time
        self.configure(text=self.display_time)

        self.after(200, self.tick)


    def tick(self):
        """ Updates the display clock every 200 milliseconds """
        
        new_time = time.strftime('%e/%m %H:%M:%S')
        
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time)
        self.after(200, self.tick)
