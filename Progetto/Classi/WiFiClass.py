import network
import time
from time import sleep


class WiFi:
    def __init__(self, hotspot, password):
        self.sta_if = network.WLAN(network.STA_IF) 
        self.hotspot=hotspot
        self.password=password
        
    def connectionWiFi(self):
        print('connessione')
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
        
   
        x = 0.1
        timeout = 6
        try:
            
            self.sta_if.connect(self.hotspot, self.password)
      
            while not self.sta_if.isconnected() and timeout>0:
                sleep(x)
                timeout = timeout - x
            
            print(timeout)
        
        except OSError as e:
            self.disconnectWiFi()
        
        #print(" Connected!")
        
    def isconnected(self):
        return self.sta_if.isconnected()
        
    def disconnectWiFi(self):
        self.sta_if.disconnect()
        self.sta_if.active(False)
        
    
        
        



