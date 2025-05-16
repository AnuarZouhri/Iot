import network
import time
from time import sleep


class WiFi:
    def __init__(self, hotspot, password):
        self.sta_if = network.WLAN(network.STA_IF) 
        self.hotspot=hotspot
        self.password=password
        
    def connectionWiFi(self):
        print("Connecting to WiFi")

        if not self.sta_if.isconnected():
            self.sta_if.active(True)
        
   
    
        try:
            
            self.sta_if.connect(self.hotspot, self.password)
            
            if not self.sta_if.isconnected():
                sleep(1.5)
                
        
        except OSError as e:
            self.disconnectWiFi()
        
        #print(" Connected!")
        
    def isconnected(self):
        return self.sta_if.isconnected()
        
    def disconnectWiFi(self):
        self.sta_if.disconnect()
        self.sta_if.active(False)
        
    
        
        



