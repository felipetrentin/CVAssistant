import paho.mqtt.client as mqtt
import dicts
class Coms:
    def __init__(self, host, port):
        self.client = mqtt.Client()
        self.client.connect_async(host, port, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("ac1/temp")
        
    def on_message(self, client, userdata, msg):
        if(msg.topic == "ac1/temp"):
            dicts.devices["ac1"]["temp"] = int(msg.payload)
            main.p1.Update
        print(msg.topic+" "+str(msg.payload))
    
    def stop(self):
        self.client.loop_stop(force=False)
