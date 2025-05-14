import network
import time
from time import sleep

class WiFi:
    def __init__(self, hotspot, password):
        self.sta_if = network.WLAN(network.STA_IF)
        self.hotspot=hotspot
        self.password=password
        
    def connectionWifi(self):
        print("Connecting to WiFi", end="")
        
        self.sta_if.active(True)
        self.sta_if.connect(self.hotspot, self.password)
        print(" Connected!")
        
    
        
        
        
        


