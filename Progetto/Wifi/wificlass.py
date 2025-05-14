import framebuf
import network
import time
from time import sleep
import ujson
from umqtt.simple import MQTTClient


class WiFi:
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        
    def connectionWifi(self):
        print("Connecting to WiFi", end="")
        
        self.sta_if.active(True)
        self.sta_if.connect('Galaxy A5173BB', 'aaaaaaab')
        while not self.sta_if.isconnected():
          
          print(".", end="")
          time.sleep(0.3)
        print(" Connected!")
    
    #def disconnectWifi(self):
        
    
        
        
        
        

